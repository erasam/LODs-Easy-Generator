# Add-on parameters

The **LODs Easy Generator** custom Blender add-on allows the selection of the following parameters:

![Parameters](./images/Parameters.jpg)

- **Search by**:
  - "Collections" / "Meshes"
- **Search Filter**:
  - "All" / "By Name"
- **Name Filter** -> if "Search by Meshes" the **Name Filter** also accept wildcar
- Number of Iterations:
  - **LODs Start** with a value between 0 and 9
  - **LODs End** with a value between 0 and 9
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
- **Directory** that must be a full path reference
- **Filename** used to create the LODs filename (it can include the .blend extension)

# Add-on workflow
The **LODs Easy Generator** add-on implements the following workflow:
1. Retrieve list of Mesh objects in the Blender file being edited matching the selection parameters:
   - If "Collections" and "By Name" have been selected the retrieved meshes are all belonging to the collection identified by its Name property matching the **Name Filter** (no wildcard is allowed)
   - If "Meshes" and "By Name" have been selected the retrieved meshes are all the ones identified by their Name matching the **Name Filter** (also using wildcard)
   - In all other cases just select all meshes

2. For each iteration between **LOD Start** and **LOD End** (both included)
  - If **Enable Collections by Iterations** is selected then:
    - It enables all the collections (and belonging meshes) having its Name property containing "LOD0"+current iteration
    - It disables all the collections (and belonging meshes) having its Name property containing "LOD0"+a different iteration

  - If **Delete existing Decimate modifier** is selected it deletes all Decimate modifiers associated to it

  - If **Apply all modifiers** is selected it applies all the modifiers associated to it

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
