# Add-on parameters

The **LODs Easy Generator** custom Blender add-on allows the selection of the following parameters:

![Parameters](./images/Parameters.jpg)

- **Search by**:
  - "Collections" / "Meshes"
- **Search Filter**:
  - "All" / "By Name"
- **Name Filter** -> if "Search by Meshes" the **Name Filter** also accept wildcar
- Number of Iterations (from **LODs Start** to **LODs End**)
- **Enable Collections by Iterations** (Y/N)
- **Subdiv Modifiers**:
  - "Leave"
  - "Reduce Level"
  - "Delete"
- **Delete existing Decimate Modifiers** ("Y" / "N")
- **Apply all Modifiers** ("Y" / "N")
- **Decimate Type** ("Collapse" / "Un-subdivide" / "Planar")
- Decimate Parameters (by **Decimate type**):
  - "Collapse":
    - **Collapse Ratio**
    - **Collapse Triangulate**
  - "Un-Subdivide":
    - **Un-Subdivide Iterations**
  - "Planar":
    - **Planar Angle Limit** 
    - **Delimit** ("None" / "Normal" / "Seam" / "Sharp" / "UVs")
    - **All Boundaries** ("Y" / "N")
- **Directory**
- **Filename**

# Add-on workflow
The **LODs Easy Generator** add-on implements the following workflow:
1. Retrieve list of Mesh objects in the Blender file being edited matching selection parameters
   - If "Collections" and "By Name" have been selected the retrieved meshes are all belonging to the collection identified by its Name property
   - If "Meshes" and "By Name" have been selected the retrieved meshes are all the ones identified by their Name matching the **Name Filter** (also using wildcard)
   - In all other case just select all meshes

2. For each iteration between **LOD Start** and **LOD End**
  - If **Enable Collections by Iterations** is Yes then:
    - It enables all the collections (and belonging meshes) having the Name containng the "LOD0"+iteration
    - It disables all the collections (and belonging meshes) having the Name containng the "LOD0"+iteration
   - If "Delete existing Decimate modifier" it deletes all Decimate modifiers associated to it
   - If "Apply all modifiers" it applies all the modifiers associated to it
   - It appends a new Decimate modifier to the selected mesh having
    - Name="LOD"+"str(iteration+1)"
    - Type="Decimate type"
    - Ratio based on "Decimate ratio"   //depending on "Decimate Type" e.g. for Collapse 1-decimateRatio*(iteration+1) 

- If "Save file" it saves a new blender file with same source name + LODiteration   //e.g. format(fileName, "_LOD",str(iteration+1),".blend")
- If "Open created file" it invokes a new blender instance to open the created file

# Add-on execution
With the parameters shown in the previous picture, the **Generate LOD files** button will create two files as shown in the following pictures:

![LODSfiles](./images/LODs_files.jpg)

![LODsIteration0](./images/LODs_Iteration_0.jpg)

![LODsIteration1](./images/LODs_Iteration_1.jpg)
