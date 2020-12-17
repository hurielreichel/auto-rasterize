#!/usr/bin/env python3
#  auto-rasterize
#
#     Huriel Reichel - huriel.ruan@gmail.com
#     Nils Hamel - nils.hamel@bluewin.ch
#     Copyright (c) 2020 Republic and Canton of Geneva
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gdal
import ogr
import argparse

pm_argparse = argparse.ArgumentParser()

# argument and parameter directive #
pm_argparse.add_argument( '-i', '--input', type=str  , help='shapefile path'    )
pm_argparse.add_argument( '-o', '--output' , type=str  , help='GeoTiff output path' )
pm_argparse.add_argument( '-r', '--ref', type=str  , help='GeoTiff file for x and y reference, if needed'    )
pm_argparse.add_argument( '--xmin' , type=float  , help='minimum X / Longitude value' )
pm_argparse.add_argument( '--ymin' , type=float  , help='minimum Y / Latitude value' )
pm_argparse.add_argument( '--xmax' , type=float  , help='maximum X / Longitude value' )
pm_argparse.add_argument( '--ymax' , type=float  , help='minimum Y / Latitude value' )
pm_argparse.add_argument( '-p' , '--pixel', type=float  , help='output pixel size' )

# read argument and parameters #
pm_args = pm_argparse.parse_args()    


def rasterize(input, output, xmin, ymin, xmax, ymax, pixel):
    # Open the data source
    orig_data_source = ogr.Open(input)
    # Make a copy of the layer's data source because we'll need to 
    # modify its attributes table
    source_ds = ogr.GetDriverByName("Memory").CopyDataSource(
            orig_data_source, "")
    source_layer = source_ds.GetLayer(0)
    source_srs = source_layer.GetSpatialRef() 
    

    # Create the destination data source
    x_res = int((xmax - xmin) / pixel)
    y_res = int((ymax - ymin) / pixel)      
    
    target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res,
            y_res, 3, gdal.GDT_Byte)
    target_ds.SetGeoTransform((
            xmin, pixel, 0,
            ymax, 0, -pixel,
        ))
    target_ds.GetRasterBand(1).SetNoDataValue(0)
    target_ds.GetRasterBand(2).SetNoDataValue(0)
    target_ds.GetRasterBand(3).SetNoDataValue(0)
    if source_srs:
        # Make the target raster have the same projection as the source
        target_ds.SetProjection(source_srs.ExportToWkt())
    else:
        # Source has no projection (needs GDAL >= 1.7.0 to work)
        target_ds.SetProjection('LOCAL_CS["arbitrary"]')
    # Rasterize
    err = gdal.RasterizeLayer(target_ds, (3, 2, 1), source_layer,
            burn_values=(255, 255, 255))
    if err != 0:
        raise Exception("error rasterizing layer: %s" % err)

if (pm_args.ref == None):
    print('rasterizing based on given coordinates')
    rasterize(pm_args.input, pm_args.output, pm_args.xmin, pm_args.ymin, pm_args.xmax, pm_args.ymax, pm_args.pixel)
    
else:
    print('rasterizing based on reference raster')

    # Retrieve data from reference raster        
    rst = gdal.Open(pm_args.ref)

    # Resolution
    pm_width = rst.RasterXSize
    pm_height = rst.RasterYSize

    pm_gtrans = rst.GetGeoTransform()

    # retrieve raster geographic parameters #
    xmin = pm_gtrans[0] # origin x #
    ymax = pm_gtrans[3] # origin y #
    pm_pw = pm_gtrans[1] # pixel width #
    pm_ph = -pm_gtrans[5] # pixel height #
    xmax = xmin + pm_pw * pm_width
    ymin = ymax - pm_ph * pm_height

    rasterize(pm_args.input, pm_args.output, xmin, ymin, xmax, ymax, pm_args.pixel)
    
