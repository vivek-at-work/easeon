# -*- coding: utf-8 -*-
import datetime
import json

import pytz
from django.conf import settings
# from openpyxl import Workbook
# from openpyxl.drawing.image import Image
# from openpyxl.styles import (
#     Alignment,
#     Border,
#     Font,
#     NamedStyle,
#     PatternFill,
#     Side,
# )
# from openpyxl.utils import get_column_letter
# from openpyxl.writer.excel import save_virtual_workbook
from rest_framework.renderers import (BaseRenderer, BrowsableAPIRenderer,
                                      JSONRenderer)
from rest_framework.utils import encoders


class XLSXFileMixin(object):
    """
    Mixin which allows the override of the filename being
    passed back to the user when the spreadsheet is downloaded.
    """

    filename = 'export.xlsx'

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(XLSXFileMixin, self).finalize_response(
            request, response, *args, **kwargs
        )
        if response.accepted_renderer.format == 'xlsx':
            response['content-disposition'] = 'attachment; filename={}'.format(
                self.filename
            )
        return response


class BrowsableAPIRenderer(BrowsableAPIRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        parent = super(BrowsableAPIRenderer, self)
        context = parent.get_context(
            data, accepted_media_type, renderer_context
        )
        context['SITE_HEADER'] = settings.SITE_HEADER
        return context


class JSONEncoder(encoders.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            obj = obj.astimezone(pytz.utc)
        return super(JSONEncoder, self).default(obj)


class JSONRenderer(JSONRenderer):
    def get_context(self, data, accepted_media_type, renderer_context):
        parent = super(BrowsableAPIRenderer, self)
        context = parent.get_context(
            data, accepted_media_type, renderer_context
        )
        context['SITE_HEADER'] = settings.SITE_HEADER
        return context


# def get_style_from_dict(style_dict, style_name):
#     """
#     Make NamedStyle instance from dictionary
#     :param style_dict: dictionary with style properties.
#            Example:    {'fill': {'fill_type'='solid',
#                                  'start_color'='FFCCFFCC'},
#                         'alignment': {'horizontal': 'center',
#                                       'vertical': 'center',
#                                       'wrapText': True,
#                                       'shrink_to_fit': True},
#                         'border_side': {'border_style': 'thin',
#                                         'color': 'FF000000'},
#                         'font': {'name': 'Arial',
#                                  'size': 14,
#                                  'bold': True,
#                                  'color': 'FF000000'}
#                         }
#     :param style_name: name of created style
#     :return: openpyxl.styles.NamedStyle instance
#     """
#     style = NamedStyle(name=style_name)
#     if not style_dict:
#         return style
#     for key, value in style_dict.items():
#         if key == 'font':
#             style.font = Font(**value)
#         elif key == 'fill':
#             style.fill = PatternFill(**value)
#         elif key == 'alignment':
#             style.alignment = Alignment(**value)
#         elif key == 'border_side':
#             side = Side(**value)
#             style.border = Border(left=side, right=side, top=side, bottom=side)

#     return style


# def get_attribute(get_from, prop_name, default=None):
#     """
#     Get attribute from object with name <prop_name>, or take it from function get_<prop_name>
#     :param get_from: instance of object
#     :param prop_name: name of attribute (str)
#     :param default: what to return if attribute doesn't exist
#     :return: value of attribute <prop_name> or default
#     """
#     prop = getattr(get_from, prop_name, None)
#     if not prop:
#         prop_func = getattr(get_from, 'get_{}'.format(prop_name), None)
#         if prop_func:
#             prop = prop_func()
#     if prop is None:
#         prop = default
#     return prop


# class XLSXRenderer(BaseRenderer):
#     """
#     Renderer for Excel spreadsheet open data format (xlsx).
#     """

#     media_type = 'application/xlsx'
#     format = 'xlsx'

#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         """
#         Render `data` into XLSX workbook, returning a workbook.
#         """
#         if not self._check_validatation_data(data):
#             return self._json_format_response(data)

#         if data is None:
#             return bytes()

#         wb = Workbook()
#         ws = wb.active

#         results = data['results'] if 'results' in data else data

#         # Take header and column_header params from view
#         header = get_attribute(renderer_context['view'], 'header', {})
#         ws.title = header.get('tab_title', 'Report')
#         header_title = header.get('header_title', 'Report')
#         img_addr = header.get('img')
#         if img_addr:
#             img = Image(img_addr)
#             ws.add_image(img, 'A1')
#         header_style = get_style_from_dict(header.get('style'), 'header_style')

#         column_header = get_attribute(
#             renderer_context['view'], 'column_header', {}
#         )
#         column_header_style = get_style_from_dict(
#             column_header.get('style'), 'column_header_style'
#         )

#         column_count = 0
#         row_count = 1
#         if header:
#             row_count += 1
#         # Make column headers
#         column_titles = column_header.get('titles', [])
#         if results:
#             for column_name in results[0].keys():
#                 if column_name == 'row_color':
#                     continue
#                 column_count += 1
#                 if column_count > len(column_titles):
#                     column_name_display = column_name
#                 else:
#                     column_name_display = column_titles[column_count - 1]

#                 ws.cell(
#                     row=row_count,
#                     column=column_count,
#                     value=column_name_display,
#                 ).style = column_header_style
#             ws.row_dimensions[row_count].height = column_header.get(
#                 'height', 45
#             )

#         # Set the header row
#         if header:
#             last_col_letter = 'G'
#             if column_count:
#                 last_col_letter = get_column_letter(column_count)
#             ws.merge_cells('A1:{}1'.format(last_col_letter))

#             cell = ws.cell(row=1, column=1, value=header_title)
#             cell.style = header_style
#             ws.row_dimensions[1].height = header.get('height', 45)

#         # Set column width
#         column_width = column_header.get('column_width', 20)
#         if isinstance(column_width, list):
#             for i, width in enumerate(column_width):
#                 col_letter = get_column_letter(i + 1)
#                 ws.column_dimensions[col_letter].width = width
#         else:
#             for ws_column in range(1, column_count + 1):
#                 col_letter = get_column_letter(ws_column)
#                 ws.column_dimensions[col_letter].width = column_width

#         # Make body
#         body = get_attribute(renderer_context['view'], 'body', {})
#         body_style = get_style_from_dict(body.get('style'), 'body_style')
#         for row in results:
#             column_count = 0
#             row_count += 1
#             for column_name, value in row.items():
#                 if column_name == 'row_color':
#                     continue
#                 column_count += 1
#                 cell = ws.cell(
#                     row=row_count,
#                     column=column_count,
#                     value='{}'.format(value),
#                 )
#                 cell.style = body_style
#             ws.row_dimensions[row_count].height = body.get('height', 40)
#             if 'row_color' in row:
#                 last_letter = get_column_letter(column_count)
#                 cell_range = ws[
#                     'A{}'.format(row_count) : '{}{}'.format(
#                         last_letter, row_count
#                     )
#                 ]
#                 fill = PatternFill(
#                     fill_type='solid', start_color=row['row_color']
#                 )
#                 for r in cell_range:
#                     for c in r:
#                         c.fill = fill

#         return save_virtual_workbook(wb)

#     def _check_validatation_data(self, data):
#         detail_key = 'detail'
#         if detail_key in data:
#             return False
#         return True

#     def _json_format_response(self, response_data):
#         return json.dumps(response_data)
