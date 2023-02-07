# shp2jvmapgen
Python library for generating jvectormap-based maps from shapefiles or GeoJSON, including the user's selected fields from the source file to become the id and name of the polygon in the jvectormap. This library runs on Python 3.

A shapefile, in simpler terms, is like a digital map that contains information about the shapes and locations of various features. Think of it as a digital filing cabinet, storing information about roads, buildings, rivers, and other features that make up the geography of a region. It’s not just a static image, but a dynamic collection of data that can be used to analyze and understand the world around us. Whether it's for city planning, environmental studies, or even video game design, the shapefile is a powerful tool that provides a way to represent and analyze real-world data in a spatial context.

GeoJSON is a geographic data interchange format based on JavaScript Object Notation (JSON). It is used to represent various types of geographic features such as points, lines, and polygons (referred to as "features"), and their properties. GeoJSON features are specified with a set of coordinates and optional properties, and can be easily integrated into web-based maps and GIS systems. GeoJSON is a widely used format for encoding and sharing spatial data on the web and is supported by many software libraries and tools for web mapping, data analysis, and spatial data processing.

jVectorMap is a library for creating interactive vector maps on a web page. It's like having a digital world map at your fingertips, where you can zoom in, zoom out, and even highlight different regions. But what makes jVectorMap different from a regular map is that it's designed to be used in web applications, meaning you can easily add it to your website or web-based project. With jVectorMap, you can display information in a way that's both visually appealing and interactive, allowing your users to explore the data and gain insights in a fun and engaging way. So, whether you're working on a data visualization project, creating a geography quiz, or just looking for an interactive way to display information, jVectorMap is a tool worth checking out.

jVectorMap relies on JavaScript to work and it only supports its own format for map data. This means that in order to use jVectorMap, you'll need to provide it with a map in jVectorMap format or convert an existing map into this format. And this is the python library to convert your shapefiles into jvectormaps.

# installation
You can install this library using pip

  	  pip install shp2jvmapgen

Then, import the library to your python console:

  	  from shp2jvmapgen import shp2jvmap as s2jvm
      
The library use JVMapgenerator class to make new object, then convert your source file to jvectormap while setting the width pixel to apply into your jvectormap

JVMapgenerator:

  First, you need to inisiate the class.
      
      # default source file format is shapefile
      generator = s2jvm.JVMapGenerator()
      # for GeoJSON source file format
      generator = s2jvm.JVMapGenerator(sourceformat = "geojson")
  
  Continue to shapefile exploration function. Use printFields() method to know the layer fields names. With this method you can  
  print all fields of your shapefile, then you can choose and use them as jvectormap polygon id and name attributes.
      
      # for shapefile source file format
  	  generator.printFields('path/to/file.shp')
      # for GeoJSON source file format
      generator.printFields('path/to/file.geojson')
  
  Once you have selected your id and name, you have to call run() method. This function require 5 parameters: The input 
  file path, the output file path, name and id as you've choosen and width pixel value that is an integer or float, like you can see below. This method will create the jvectormap file in the defined output file path.

      width_pixel = 800
      id_field = 'ID'
      name_field = 'Region_Name'
      input_file= 'path/to/input_file.shp'      # change the input file path to your file, if its a Geojason
      output_file = 'path/to/output_file.js'

  	  generator.run(input_file, output_file, id_field, name_field, width_pixel)