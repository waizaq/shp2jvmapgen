from pathlib import Path
import random
import shapefile
from . import bound2pixel
from . import svg2jvm

class JVMapGenerator:
    def __init__(self):
        self.width_pixels = 800

    def writeToFile(self, ofile, jvmap):
        jvmap_filename = ofile.split('.')[0] + '.js'
        output = jvmap
        file = open(jvmap_filename, "wb")
        for line in output:
            file.write(line.encode('utf-8'))
        file.close()
        print ('Jvectormap generated: ' + jvmap_filename)

    def encode_svg(self, svg):
        content = bytes()
        for line in svg:
            content = content + line.encode('utf-8')        
        return content


    def printFields(self, ifile):
        fieldsList = []
        layer = shapefile.Reader(ifile)
        for field in layer.fields:
            if type(field) is tuple:
                continue
            else:
                fieldsList.append(field[0])

        print
        print (fieldsList)
        print

    def feature2svg(self, feature, field_num, field_num2, layer_extent, mupp):
        geom = feature[1]
        id = str(feature[0][field_num])
        name = str(feature[0][field_num2])
        svgGroup = [u'<path d="']

        if len(geom.parts) == 1:
            svgGroup.extend(self.polygon2path(geom, layer_extent, mupp))
        elif len(geom.parts) > 1:
            svgGroup.extend(self.multiPolygon2path(geom, layer_extent, mupp))
        else:
            pass

        svgGroup.append('" fill-rule="evenodd" id="'+id+'" name="'+name+'"/>\n')

        return svgGroup

    def multiPolygon2path(self, geom, layer_extent, mupp):
        svgPolygon = []
        geom.parts.append(len(geom.points))
        poly_list = []
        parts_counter = 0

        while parts_counter < len(geom.parts) - 1:
            coord_count = geom.parts[parts_counter]
            no_of_points = abs(geom.parts[parts_counter] - geom.parts[parts_counter + 1])
            part_list = []
            end_point = coord_count + no_of_points
            while coord_count < end_point:
                for coords in geom.points[coord_count:end_point]:
                    x, y = coords[0], coords[1]
                    poly_coord = [float(x), float(y)]
                    part_list.append(poly_coord)
                    coord_count = coord_count + 1
            poly_list.append(part_list)
            parts_counter = parts_counter + 1

        for ring in poly_list:
            svgPath = 'M '
            last_pixel = [0, 0]
            coordCount = 0

            for latLng in ring:
                x, y = latLng[0], latLng[1]
                if layer_extent[0] > 0 and layer_extent[2] > 0 or layer_extent[0] > 0 and layer_extent[2] > 0:
                    pixpoint = self.w2p(x, y, abs(layer_extent[0] - layer_extent[2]) / mupp, layer_extent[0],
                                        layer_extent[3])
                else:
                    pixpoint = self.w2p(x, y, (abs(layer_extent[0]) + abs(layer_extent[2])) / mupp, layer_extent[0],
                                        layer_extent[3])

                if last_pixel != pixpoint:
                    coordCount += 1
                    if coordCount > 1:
                        svgPath += ''
                    svgPath += (str(pixpoint[0]) + ' ' + str(pixpoint[1]) + ' ')
                    last_pixel = pixpoint

            if coordCount > 2:
                svgPath += 'Z '
                svgPolygon.extend([svgPath])

        return svgPolygon

    def polygon2path(self, geom, layer_extent, mupp):
        svgPolygon = []
        svgPath = 'M '
        last_pixel = [0, 0]
        coordCount = 0

        for latLng in geom.points:
            x, y = latLng[0], latLng[1]
            if layer_extent[0] > 0 and layer_extent[2] > 0 or layer_extent[0] > 0 and layer_extent[2] > 0:
                pixpoint = self.w2p(x, y, abs(layer_extent[0] - layer_extent[2]) / mupp, layer_extent[0], layer_extent[3])
            else:
                pixpoint = self.w2p(x, y, (abs(layer_extent[0]) + abs(layer_extent[2])) / mupp, layer_extent[0],
                                    layer_extent[3])

            if last_pixel != pixpoint:
                coordCount += 1
                if coordCount > 1:
                    svgPath += ''
                svgPath += (str(pixpoint[0]) + ' ' + str(pixpoint[1]) + ' ')
                last_pixel = pixpoint

        if coordCount > 2:
            svgPath += 'Z '
            svgPolygon.extend([svgPath])

        return svgPolygon

    def w2p(self, x, y, mupp, minx, maxy):
        pix_x = (x - minx) / mupp
        pix_y = (y - maxy) / mupp
        return [round(float(pix_x), 1), round(float(-pix_y), 1)]

    def run(self, in_file, out_path, id_name, name_name, width_pixel):
        if(width_pixel > 0):
            self.width_pixels = width_pixel
        layer = shapefile.Reader(in_file)
        out_file = out_path
        field_name = id_name
        count_fields = 0
        field_num = 0
        mupp = self.width_pixels
        for field in layer.fields:
            if type(field) is tuple:
                continue
            else:
                if field[0] == field_name:
                    field_num = count_fields
                else:
                    count_fields += 1

        field_name2 = name_name
        count_fields2 = 0
        field_num2 = 0
        for field2 in layer.fields:
            if type(field2) is tuple:
                continue
            else:
                if field2[0] == field_name2:
                    field_num2 = count_fields2
                else:
                    count_fields2 += 1
        
        # Generate width and height of svg file
        converter = bound2pixel.Converter(in_file, self.width_pixels)
        width,height = converter.converttopx()

        # Generate the bounding box of shapefile
        layer_extent = layer.bbox

        # Generate the geometry layer
        records = layer.records()
        shapes = layer.shapes()

        features = zip(records, shapes)

        # Converting and formatting the svg file output
        svg = [u'<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n']
        svg.append(
            u'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
        svg.append(u'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" baseProfile="tiny" width="'+str(width)+'" height="'+str(height)+'" stroke-linecap="round" stroke-linejoin="round">\n')
        svg.append(u'<g id="' + str(random.randint(10,100)) + '">\n')
        for feature in features:
            svg.extend(self.feature2svg(feature, field_num, field_num2, layer_extent, mupp))
        
        svg.append('</g>\n')
        svg.append(u'</svg>')

        jvm = svg2jvm.Map()
        jvm.load_from_svg(self.encode_svg(svg))
        jv_map = jvm.get_result(Path(out_file).stem)

        self.writeToFile(out_file, jv_map)
