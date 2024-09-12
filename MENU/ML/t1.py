import kivy
kivy.require('2.1.0')  # Replace with your Kivy version

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window  # Import Window to manage the application window
from tkinter import Tk, filedialog
import pandas as pd
import pickle
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from threading import Thread

class ModelTrainerApp(App):
    def build(self):
        self.file_path = ""
        self.model_file = "model.pkl"
        self.loading_popup = None
        
        # Set the window icon
        Window.set_icon('MENU/assets/ml.png')
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # File path input
        self.file_entry = TextInput(hint_text='CSV File Path', readonly=True, size_hint_y=None, height=40)
        layout.add_widget(self.file_entry)
        
        # Browse button
        browse_btn = Button(text='Browse', size_hint_y=None, height=40)
        browse_btn.bind(on_press=self.open_file_dialog)
        layout.add_widget(browse_btn)
        
        # Process and Train button
        process_btn = Button(text='Process and Train', size_hint_y=None, height=40)
        process_btn.bind(on_press=self.process_and_train)
        layout.add_widget(process_btn)
        
        # Result display area
        result_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.result_area = TextInput(size_hint_y=0.8, readonly=True, multiline=True)
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.result_area)
        result_layout.add_widget(scroll_view)
        
        layout.add_widget(result_layout)
        
        return layout
    
    def open_file_dialog(self, instance):
        root = Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.file_path = file_path
            self.file_entry.text = self.file_path
    
    def show_loading_popup(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        spinner = Label(text='Processing...', size_hint=(1, 1), size=(100, 100))
        content.add_widget(spinner)
        self.loading_popup = Popup(title='Please Wait', content=content, size_hint=(None, None), size=(200, 200))
        self.loading_popup.open()
    
    def hide_loading_popup(self):
        if self.loading_popup:
            self.loading_popup.dismiss()
    
    def process_and_train(self, instance):
        if not self.file_path:
            self.result_area.text = "Error: Please select a CSV file first."
            return
        
        self.show_loading_popup()
        Thread(target=self.process_and_train_in_background).start()
    
    def process_and_train_in_background(self):
        processed_file = "processed_file.csv"
        process_csv(self.file_path, processed_file)
        
        result = train_model(processed_file, self.model_file)
        
        Clock.schedule_once(lambda dt: self.update_result_area(result), 0)
        Clock.schedule_once(lambda dt: self.hide_loading_popup(), 0)

    def update_result_area(self, result):
        self.result_area.text = result

def process_csv(file_path, output_file='processed_file.csv', id_cols=None):
    try:
        try:
            df = pd.read_csv(file_path)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
        except pd.errors.ParserError:
            df = pd.read_csv(file_path, error_bad_lines=False, warn_bad_lines=True)
        
        print("CSV file read successfully.")

        if id_cols:
            id_data = df[id_cols]
            features = df.drop(columns=id_cols)
        else:
            features = df
        
        features = df.iloc[:, :-1]
        target = df.iloc[:, -1]

        numeric_cols = features.select_dtypes(include=['number']).columns
        categorical_cols = features.select_dtypes(include=['object', 'category']).columns

        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_cols),
                ('cat', categorical_transformer, categorical_cols)
            ])

        X_processed = preprocessor.fit_transform(features)

        onehot_feature_names = preprocessor.named_transformers_['cat']['onehot'].get_feature_names_out(categorical_cols)

        processed_feature_names = numeric_cols.tolist() + onehot_feature_names.tolist()

        X_processed_df = pd.DataFrame(X_processed, columns=processed_feature_names)

        if not target.empty:
            processed_df = pd.concat([X_processed_df, target.reset_index(drop=True)], axis=1)
        else:
            processed_df = X_processed_df

        if id_cols:
            processed_df = pd.concat([id_data.reset_index(drop=True), processed_df], axis=1)

        processed_df.to_csv(output_file, index=False)
        print(f"\nProcessed data saved to {output_file}.")

    except Exception as e:
        print(f"An error occurred while processing the file: {str(e)}")

def train_model(processed_file_path, model_file='model.pkl'):
    try:
        df = pd.read_csv(processed_file_path)
        
        target = df.iloc[:, -1]
        features = df.iloc[:, :-1]
        
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(random_state=42)
        
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
        
        grid_search.fit(X_train, y_train)
        
        best_model = grid_search.best_estimator_
        
        with open(model_file, 'wb') as f:
            pickle.dump(best_model, f)
        
        y_pred = best_model.predict(X_test)
        
        results = []
        results.append("\nBest Parameters from Grid Search:")
        results.append(str(grid_search.best_params_))
        
        results.append("\nModel evaluation:")
        results.append(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        results.append("Classification Report:")
        results.append(classification_report(y_test, y_pred))
        
        cv_scores = cross_val_score(best_model, features, target, cv=5)
        results.append("\nCross-validation scores:")
        results.append(str(cv_scores))
        results.append(f"Mean CV Score: {cv_scores.mean()}")
        
        return "\n".join(results)

    except Exception as e:
        return f"An error occurred while training the model: {str(e)}"

if __name__ == "__main__":
    ModelTrainerApp().run()
