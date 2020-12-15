# Overview
This tool allows one to rasterize a shapefile, automatically turning it into a binary GeoTiff file. This is usefull when creating ground truth dataset for image segmentation and/or object detection. The thought use case was transforming polygons of the houses in Switzerland into raster with a croping argument.

## auto-rasterize
In order to use this code, the main arguments are input shapefile path, output GeoTiff (.tif) file path and crop arguments. Of those, you'll have minimum X (longitude), minimum Y (latitude), maximum X and maximum Y. At last, the pixel size shall be defined as well. 

The following exemplifies the code usage in a linux terminal in the CH1903+ Swiss Coordinate System.

```
$python3 auto_rasterize.py -i /path/to/shapefile.shp -o /path/to/output/GeoTiff.tif -xmin 2709756 --ymin 1268735 --xmax 2711300 --ymax 1270009 -p 10
```

The figure below demonstrates a polygon of houses in Frauenfeld (TG - Switzerland) - image on the left -  being rasterized and croped to a specific extent - image on the right.

![](example.png)

# Copyright and License

las-to-uv3 - Huriel Reichel Nils Hamel
Copyright (c) 2020 Republic and Canton of Geneva

This program is licensed under the terms of the GNU GPLv3. Documentation and illustrations are licensed under the terms of the CC BY-NC-SA.

