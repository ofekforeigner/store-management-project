from fpdf import FPDF
import sys
from datetime import datetime
from Xml import Xml
from pathlib import Path
import re


class Pdf:
    def __init__(self, report_type, header, total_quantity_name, start_date, end_date):
        self.url = "reports"
        self.col_width = 0
        self.header = header
        self.business_info = Xml().business_details_get()
        # GETS THE ID OF THE REPORT IN ORDER TO KNOW WHICH REPORT TO SAVE
        self.report_type = report_type
        self.total_quantity_name = total_quantity_name
        self.start_date = start_date
        self.end_date = end_date

        self.create_pdf_page()
        self.insert_date_to_pdf()  # insert date to pdf.
        self.insert_business_info_to_pdf()  # insert business info.
        self.insert_report_name_to_pdf()  # inser report name.

    def create_pdf_page(self):
        self.pdf = FPDF('P', 'mm', 'A4')
        self.pdf.add_page()
        self.page_width = self.pdf.w - 4 * self.pdf.l_margin

    def insert_date_to_pdf(self):
        ###-----------------------date-------------------------###
        self.pdf.add_font(
            'DejaVuSansCondensed', '', 'Fonts\DejaVuSansCondensed.ttf', uni=True)
        self.pdf.set_font('DejaVuSansCondensed', '', 10)
        self.pdf.cell(self.page_width, -15,
                      datetime.today().strftime('%d-%m-%Y') + u"ךיראת")
        self.pdf.ln(3)

    def insert_business_info_to_pdf(self):
        business_info_len = 0
        for row in self.business_info:
            if business_info_len != len(self.business_info) - 1:
                row = ''.join(s if s.isdigit() else s[::-1] for s in reversed(re.split('(\d+)', row)))
                self.pdf.cell(self.page_width, 0, row, align='R')
                self.pdf.ln(4)
                business_info_len += 1
            else:  # the last row is an email, we dont need to reverse the string
                self.pdf.cell(self.page_width, 0, row, align='R')
        self.pdf.ln(13)

    def insert_report_name_to_pdf(self):
        report_header = ''.join(s if s.isdigit() else s[::-1] for s in reversed(re.split('(\d+)', self.header)))
        self.pdf.add_font(
            'DejaVuSansCondensed', '', 'Fonts\DejaVuSansCondensed.ttf', uni=True)
        self.pdf.set_font('DejaVuSansCondensed', '', 20)
        self.pdf.cell(self.page_width, 0, report_header, align='C')
        if self.start_date and self.end_date:
            self.pdf.ln(20)
            self.insert_chosen_dates_to_pdf()
        self.pdf.ln(20)

    def insert_chosen_dates_to_pdf(self):
        ###-----------------------dates filter-------------------------###
        self.pdf.add_font(
            'DejaVuSansCondensed', '', 'Fonts\DejaVuSansCondensed.ttf', uni=True)
        self.pdf.set_font('DejaVuSansCondensed', '', 10)
        self.start_date = str(self.start_date).replace("-", "/")
        self.end_date = str(self.end_date).replace("-", "/")
        self.pdf.cell(self.page_width, -15,
                      str(self.end_date) + ' - ' + str(self.start_date), align='C')
        self.pdf.ln(1)
        ###-------------------------------------------------------###

    def save_pdf(self):
        self.pdf.output(
            self.url + "//" + self.header + datetime.today().strftime('%d-%m-%Y') + ".pdf")

    def top_5_sold_items(self, items):
        ###----------------------headers-------------------------###
        self.pdf.set_font('DejaVuSansCondensed', '', 16)
        text = [[u'שם פריט', u'מק"ט', u'כמות']]
        for txt in text[0]:
            txt = txt[::-1]
            self.pdf.set_fill_color(222, 222, 222)
            self.pdf.cell(35, 8, txt, border=1, align='C', fill=True)
        self.pdf.ln(8)

        ###-----------------------data--------------------------###
        item_list = []
        for x in items:  # change to 2d list from 2d tuple
            item_list.append(list(x))
        i = 0
        self.pdf.set_font('DejaVuSansCondensed', '', 10)
        while i < len(item_list):
            for y in item_list[i]:
                if type(y) == str:
                    k = u"" + y[::-1] + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
                else:
                    k = u"" + str(y) + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
            self.pdf.ln(8)
            i += 1
        self.pdf.ln(7)
        self.pdf.set_font('DejaVuSansCondensed', '', 12)

    def categories_to_pdf(self, categories, total):
        ###----------------------headers-------------------------###
        self.pdf.set_font('DejaVuSansCondensed', '', 16)
        text = [[u'DI', u'שם קטגורייה']]
        for txt in text[0]:
            txt = txt[::-1]
            self.pdf.set_fill_color(222, 222, 222)
            self.pdf.cell(35, 8, txt, border=1, align='C', fill=True)
        self.pdf.ln(8)

        ###-----------------------data--------------------------###
        item_list = []
        for x in categories:  # change to 2d list from 2d tuple
            item_list.append(list(x))
        i = 0
        j = 0
        self.pdf.set_font('DejaVuSansCondensed', '', 10)
        while i < len(item_list):
            for y in item_list[i]:
                if type(y) == str:
                    k = u"" + y[::-1] + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
                else:
                    k = u"" + str(y) + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
            self.pdf.ln(8)
            i += 1
        self.pdf.ln(7)
        total = str(total[0][0])
        self.pdf.set_font('DejaVuSansCondensed', '', 12)
        self.pdf.cell(15, 8, total + self.total_quantity_name)

        ###-------------------------------------------------###

    def items_in_stock_to_pdf(self, items, total):
        ###----------------------headers-------------------------###
        self.pdf.set_font('DejaVuSansCondensed', '', 16)
        text = [[u'DI', u'שם פריט', u'מק"ט', u'כמות', u'ספק']]
        for txt in text[0]:
            txt = txt[::-1]
            self.pdf.set_fill_color(222, 222, 222)
            self.pdf.cell(35, 8, txt, border=1, align='C', fill=True)
        self.pdf.ln(8)
        ###-------------------------------------------------###

        ###-----------------------data--------------------------###
        item_list = []
        for x in items:  # change to 2d list from 2d tuple
            item_list.append(list(x))
        i = 0
        j = 0
        self.pdf.set_font('DejaVuSansCondensed', '', 10)
        while i < len(item_list):
            for y in item_list[i]:
                if type(y) == str:
                    k = u"" + y[::-1] + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
                else:
                    k = u"" + str(y) + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
                # j+=1
            self.pdf.ln(8)
            i += 1

        self.pdf.ln(7)
        self.pdf.set_font('DejaVuSansCondensed', '', 12)
        # total items in stock
        if total[0][0] != None:
            self.pdf.cell(15, 8, str(total[0][0]) + self.total_quantity_name)
        else:
            self.pdf.cell(15, 8, "0" + self.total_quantity_name)

    def order_by_supplier(self, order_info, items_in_order):
        ###----------------------headers-------------------------###
        self.pdf.set_font('DejaVuSansCondensed', '', 16)
        text = [[u'שם פריט', u'מק"ט', u'כמות', u'מחיר קניה', u'סה"כ']]
        for txt in text[0]:
            txt = txt[::-1]
            self.pdf.set_fill_color(222, 222, 222)
            self.pdf.cell(35, 8, txt, border=1, align='C', fill=True)
        self.pdf.ln(8)

        ###-----------------------data--------------------------###
        item_list = []
        for x in items_in_order:  # change to 2d list from 2d tuple
            item_list.append(list(x))
        i = 0

        self.pdf.set_font('DejaVuSansCondensed', '', 10)
        while i < len(item_list):
            for y in item_list[i]:
                if type(y) == str:
                    k = u"" + y[::-1] + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
                else:
                    k = u"" + str(y) + ""
                    self.pdf.cell(35, 8, k, border=1, align='C')
            self.pdf.ln(8)
            i += 1
        self.pdf.ln(100)
        self.pdf.set_font('DejaVuSansCondensed', '', 12)
        self.pdf.cell(15, 8, str(order_info[0][7])+('סכום הזמנה:')[::-1])
        self.pdf.ln(7)
        self.pdf.cell(15, 8, str(
            order_info[0][6])+('סה"כ פריטים בהזמנה:')[::-1])
        self.pdf.ln(-180)
        self.pdf.cell(15, 8, str(order_info[0][5])+('תאריך הזמנה:')[::-1])
        self.pdf.ln(7)
        self.pdf.cell(15, 8, str(order_info[0][3])[::-1]+('סוג הזמנה:')[::-1])
