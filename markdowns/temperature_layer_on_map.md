Temperature Layer on Top of Map
===============================
There are a few approaches that I did some research and trial/error for in order to add the temperature layer on top of the map using MapBox.

*  heatmap
*  fill-color
*  raster image
*  gradient

------

### Heatmap
Despite the well-known term of "heatmap" referring to the temperatures differing in colours layered on top of a map, in the graphical sense, the term refers to mapping density. For example, when mapping population on the map, the clustered (higher density) areas will be "hotter", and the more sparse areas "cooler".

Thus, using the heatmap method does not achieve what we want to do with temperatures, because it does not take the face value of the temperature into consideration. Rather, it only visualizes the clustering of the weather stations as shown circled in green below.

![image](/static/img/markdowns/heatmap_method.JPG)

------

### Fill-Color
Using vector tiles with color fills may be able to achieve this. Assigning a specific area size in some sort of circle or polygon, then providing the temperature, this will be a map of tiles and different colors. A well-known example of this method is the US electoral map, where it shows the lead for the two parties, stronger color meaning that party leads that electoral by a wider margin.

This leaves a lot of open space where either:

*  temperature needs to be assigned to the open space tile, OR
*  closest weather station tile needs to be extended to include that tile as well.

Once these vector tiles are created (including either method above), then the map will be very flush with the displayed map.

References: 

*  [Data-Driven Fill Styling](https://blog.mapbox.com/data-driven-styling-for-fill-layers-in-mapbox-gl-js-80bb5292af4e)
*  [Interpolating Temperature from Point Data](https://stackoverflow.com/questions/60859233/generating-a-continuous-interpolated-surface-from-point-data-with-mapbox-gl-js)
*  MapBox Docs - [Add a Vector Tile Source](https://docs.mapbox.com/mapbox-gl-js/example/vector-source/)

------

### Raster Image
Creating a full size image of the temperature fluctuations and processing it as an image with several layers (for zoom-ability) is another approach that can be taken. This will require a powerful backend to generate the full size image for all data ranges (e.g. per week, per day, or per hour, etc.)

This has both pros and cons, as it requires high backend performance (depending on frequency) and lots of storage, but once the images are generated, they only need to be fetched each time they are needed. This will be very performance friendly for the client (user) side.

As a lot of raster images are created by different mapping companies, this method seems to be very popular. Below is an example of the electoral map that uses this method.

![image](/static/img/markdowns/electoral_map.png)

References: 

*  [Raster Maps](https://javascriptstore.com/2017/11/08/raster-maps/)
*  MapBox Docs - [Add a Raster Tile Source](https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/)

------

### Gradient
Generate a colour gradient based on the points. This would be a data-driven gradient created as a canvas. Then add this canvas to the map so that it is overlayed on top of it. It may not be as fine-grained as what a raster file can provide, however, is more processing-friendly. This method is a bit of a compromise between data visualization precision and performance.

Using the GitHub repo: [2D Gradient](https://github.com/dismedia/gradient2d), which calculates and displays gradient on front-end, the canvas generated can be applied to the map.

Dividing the problem into parts: start with some points and generate the gradient between them, then, overlay the canvas on a map and adjust for zoom-ability.

References:

*  [Temperature Gradient Maps with MapBox](https://blog.ndustrial.io/temperature-gradient-maps-with-mapbox-gl-9f97fb44d5f2)
*  MapBox Docs - [Add a Canvas Source](https://docs.mapbox.com/mapbox-gl-js/example/canvas-source/)

------

### Other Notes
For all methods, in order for the map to still visually appear for the users, the temperature layer on top needs to be somewhat transparent. This is mainly set by using the canvas `globalAlpha` variable between 0 (fully transparent) and 1 (fully opaque). [W3Schools Reference](https://www.w3schools.com/tags/canvas_globalalpha.asp)

However, for set images, e.g. Raster Image or Gradient method, this needs to be adjusted on the data level by changing the 4th value of each `rgba` set (r, g, b, a).

References:

*  [StackOverflow](https://stackoverflow.com/questions/8961009/canvas-globalalpha-doesnt-affect-images)
*  [Transparency on Canvas](https://www.patrick-wied.at/blog/how-to-create-transparency-in-images-with-html5canvas)

There are a lot of points that are normally fed together as arguments to functions, for example: x,y, r,g,b,a are often fed to generate the pixel color. In order to pass an array as function parameter:

`my_function.apply(this, args);`

Reference:

*  [Array as Function Args](https://stackoverflow.com/questions/2856059/passing-an-array-as-a-function-parameter-in-javascript)
