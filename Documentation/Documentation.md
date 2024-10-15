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

It implements the following workflow:

If "By meshes" is selected
 - If "By name" is selected
    - filter meshes based on mesh name matching entered pattern //e.g. "Fuselage*"
   else
    - select All meshes
else //selection by Collection
 - If "By name" is selected
    - filter meshes belonging to a collection with a name matching (if not "Exclude name pattern")/not matching (if "Exclude name pattern") entered pattern //e.g. "*LOD" or "Fuselage"
   else
    - select All meshes

For each iteration   //for iteration in range(LOD_start,LOD_end+1)
- For each selected mesh:
   - If "Delete existing Decimate modifier" it deletes all Decimate modifiers associated to it
   - If "Apply all modifiers" it applies all the modifiers associated to it
   - It appends a new Decimate modifier to the selected mesh having
    - Name="LOD"+"str(iteration+1)"
    - Type="Decimate type"
    - Ratio based on "Decimate ratio"   //depending on "Decimate Type" e.g. for Collapse 1-decimateRatio*(iteration+1) 

- If "Save file" it saves a new blender file with same source name + LODiteration   //e.g. format(fileName, "_LOD",str(iteration+1),".blend")
- If "Open created file" it invokes a new blender instance to open the created file

With the parameters shown in the previous picture, the Generate LOD files" button will create two files as shown in the following pictures:

![LODSfiles](./images/LODs_files.jpg)

![LODsIteration0](./images/LODs_Iteration_0.jpg)

![LODsIteration1](./images/LODs_Iteration_1.jpg)
