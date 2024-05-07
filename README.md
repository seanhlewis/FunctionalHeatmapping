<div align="center">

![heatmaps](https://github.com/seanhlewis/FunctionalHeatmapping/assets/96705270/8a134c92-10c5-49b8-b46c-e91950f66adc)



</div>

**Functional Heatmapping** is a visualization system for conditioned time-dependent functions. It represents the functions in real-time heatmaps and calculates their movement. It can identify when functions cross the perimeter boundary or satisfy other specified conditions, providing clear visual insight into their paths. Using this tool, Bellman’s Lost in a Forest problem to be visually verified in seconds by representing time-dependent function data in real-time heatmaps. This ensures rapid, accurate verification of solutions for any conditioned time-dependent function.

_Note: As Functional Heatmapping is being actively developed, it may occasionally generate incorrect information. I am committed to remedying these issues, and encourage you to [reach out](mailto:seanhlewis@utexas.edu?subject=Functional%20Heatmapping%20Bug%20Report&amp;body=Please%20describe%20the%20bug%20here.) if you find any instances of this._

<div align="center">

</div>

# Getting Started with Functional Heatmapping

The system offers a few starter variables for you to modify and use:
Parameters are how you may change the shape, accuracy, function, and grid size of the heatmap.
* **_Shape:_** Shape is the type of shape you want to calculate the average exit time for. Options are 'circle', 'square', 'triangle', or 'rectangle'
* **_Accuracy:_** Accuracy is the number of directions checked for the average exit time calculation. Higher accuracy means more directions are checked
* **_Function:_** Function is the type of growth function used for the trajectory. Options are 'straight_line', 'exponential', 'logarithmic', 'inverse', or 'spiral'
* **_Grid Size:_** Grid size is the number of points in the x and y directions for the heatmap. Higher grid size for finer resolution

An example to visualize a heatmap of the *straight_line* function (y=t) with accuracy *3* (2^3 directions) and grid size *25* (25^2 points) for a *circle* shape:

![image](https://github.com/seanhlewis/FunctionalHeatmapping/assets/96705270/eddbc64e-0090-481a-ab0f-5e9fbd6ab23f)

Run the code with these modified variables to visualize:
![image](https://github.com/seanhlewis/FunctionalHeatmapping/assets/96705270/e1719147-3f66-42e8-8f4c-807cdaa4b86f)


Functional Heatmapping is optimized for you to create your own functions as well. Refer to code for setting up and testing your own functions.

### Contributing

If you would like to contribute, please fork the repository, create a new branch for your feature or bug fix, and submit a pull request. Feel free to open an issue to discuss any new ideas or questions beforehand.








