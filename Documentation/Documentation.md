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

2. For each Iteration between **LOD Start** and **LOD End** (both included)
    - If **Enable Collections by Iterations** is selected then:
      - It makes visible (if hidden) in the viewport all the collections having their Name property containing "LOD0"+Iteration; it also makes visible (if hidden) all belonging meshes regardless of their Name property
        - For example in the iteration "1" it will make visible in the viewport the Collections having "LOD01" in their Name (and all belonging objects regardless of their Name)  
      - It hides from the viewport all the collections having their Name property containing "LOD0"+a different iteration; it also hide all belonging meshes regardless of their Name property
        - For example in the iteration "1" it will hide in the viewport the Collections having "LOD00" or "LOD02" in their Name (and all belonging objects regardless of their Name)

    - For each previously selected Mesh object, if visible in the viewport:
      - If **Subdiv Modifiers** is not "Leave":
        - if "Reduce" is selected it reduces by one the current Level parameter for each associated Subdiv modifier
        - if "Delete" is selected it deletes all associated Subdiv modifiers

      - If **Delete existing Decimate modifier** is selected it deletes all Decimate modifiers associated to it

      - If **Apply all modifiers** is selected it applies all the modifiers associated to it

      - It appends a new Decimate modifier to the selected mesh having:
        - Name set as "LOD0"+"iteration"
        - Type set as **Decimate type**
        - Attibutes set (by **Decimate type**) based on Decimate Parameters and in particular:
           - If "Collapse" the modifier Ratio is set as 1-**Collapse Ratio***(Iteration+1)
           - If "Un-Subdivide" the modifier Iterations is set as **Un-Subdivide Iterations***(Iteration+1)
           - If "Planar" the modifier Angle Limit is set as **Planar Angle Limit***(Iteration+1)

    - It saves a new blender file in the selected **Directory** with the name built as **Filename**+"LOD0"+"iteration"

# Add-on execution
With the parameters shown in the previous picture, the **Generate LOD files** button will create two files as shown in the following pictures:

![LODSfiles](./images/LODs_files.jpg)

![LODsIteration0](./images/LODs_Iteration_0.jpg)

![LODsIteration1](./images/LODs_Iteration_1.jpg)
