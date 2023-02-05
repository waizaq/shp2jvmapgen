import fiona

class Converter:
    def __init__(self, in_path, opt_width):
        self.file_path = in_path
        self.marginX = 0
        self.marginY = 0
        self.widthPx = opt_width
        self.heightPx = 0
        
    def converttopx(self):
        with fiona.open(self.file_path) as src:
            # Initialize variables to store the min and max x and y values
            min_x, min_y = float("inf"), float("inf")
            max_x, max_y = float("-inf"), float("-inf")
            # Loop through all features in the file
            for feature in src:
                # Get the geometry of the feature
                geometry = feature["geometry"]
                # If the geometry is a polygon or multipolygon
                if geometry["type"] in ["Polygon", "MultiPolygon"]:
                    # Get the x and y coordinates of all polygons in the geometry
                    for polygon in geometry["coordinates"]:
                        if(isinstance(polygon[0], list)):
                            for x, y in polygon[0]:
                                # Update the min and max x and y values if necessary
                                min_x, min_y = min(x, min_x), min(y, min_y)
                                max_x, max_y = max(x, max_x), max(y, max_y)
                        else :
                            x, y = polygon[0]
                            min_x, min_y = min(x, min_x), min(y, min_y)
                            max_x, max_y = max(x, max_x), max(y, max_y)
        
        # Calculate bound to pixel                    
        lat_size = abs(max_y-min_y)
        lon_size = abs(max_x-min_x)

        kx = (lon_size or lat_size or 1) / (self.widthPx - self.marginX)
        self.heightPx = self.marginY + lat_size / kx if lat_size > 0 else self.widthPx
        self.heightPx = round(float(self.heightPx),2)

        return(self.widthPx, self.heightPx)