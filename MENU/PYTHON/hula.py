import uiautomator2 as u2

# Connect to the device
d = u2.connect()

# Get the UI hierarchy
hierarchy = d.dump_hierarchy()

# Save it to a file manually
with open("hierarchy.xml", "w", encoding="utf-8") as f:
    f.write(hierarchy)
