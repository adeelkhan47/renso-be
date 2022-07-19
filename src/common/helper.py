import datetime
import logging

from fpdf import FPDF

from common.email_service import send_pdf_email
from model.company import Company
from model.email_text import EmailText
from model.front_end_configs import FrontEndCofigs
from model.item_type import ItemType
from model.order_backup import OrderBackUp
from model.voucher import Voucher


def response_structure(data, total_rows: int = None):
    response = {"objects": data}
    if total_rows is not None:
        response["total_rows"] = total_rows
    return response


def error_message(msg):
    response = {"error": {"msg": msg}}
    return response


def get_booking_taxs(bookings):
    data = {}
    for booking in bookings:
        taxs = [each.tax for each in booking.item.item_subtype.itemSubTypeTaxs]
        for tax in taxs:
            if (tax.name, tax.percentage) not in data.keys():
                data[(tax.name, tax.percentage)] = 0
            if booking.cost_without_tax:
                data[(tax.name, tax.percentage)] += (tax.percentage / 100) * booking.cost_without_tax
            else:
                data[(tax.name, tax.percentage)] += (tax.percentage / 100) * booking.cost
    return data


def get_pdf(company, bookings, order):
    #
    custom_values_dict = {}
    custom_values = [x.custom_data for x in order.order_custom_data]
    for each in custom_values:
        custom_values_dict[each.name] = each.value
    street = ""
    number = ""
    zipcode = ""
    city = ""
    if "street" in custom_values_dict.keys():
        street = custom_values_dict.get("street")
    elif "Straße" in custom_values_dict.keys():
        street = custom_values_dict.get("Straße")

    if "number" in custom_values_dict.keys():
        number = custom_values_dict.get("number")
    elif "Nummer" in custom_values_dict.keys():
        number = custom_values_dict.get("Nummer")

    if "Zip Code" in custom_values_dict.keys():
        zipcode = custom_values_dict.get("Zip Code")
    elif "PLZ" in custom_values_dict.keys():
        zipcode = custom_values_dict.get("PLZ")

    if "city" in custom_values_dict.keys():
        city = custom_values_dict.get("city")
    elif "Stadt" in custom_values_dict.keys():
        city = custom_values_dict.get("Stadt")

    header = [("Item Category", 31.5), ("Location", 31.5), ("Start Time", 36.5), ("End Time", 36.5), ("Tax", 36.5),
              ("Price", 15.5)]
    # row = ["Simple Boat", "Hamburg", str(datetime.date.today()), str(datetime.date.today()), f'78.22 {chr(128)}']
    pdf = FPDF()
    pdf.add_page()

    app_configs = FrontEndCofigs.get_by_user_id(order.user_id)
    logo = app_configs.logo

    # Font
    pdf.set_font("Arial", size=10)

    # logo Part
    pdf.cell(110, 10, txt="", border=0, ln=0, align="L")
    pdf.image(w=80, h=40, name=logo)
    pdf.cell(0, h=0, txt='', border=0, ln=1, align='C')
    pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')

    pdf.set_font("Arial", size=14)
    # company Info
    pdf.cell(190, 5,
             txt=f"{company.name}, {company.street} {company.street_number}, {company.zipcode} {company.city}",
             border=0,
             ln=1,
             align="L")
    pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')

    # customer_info
    pdf.cell(190, 5, txt=order.client_name, border=0, ln=1, align="L")
    pdf.cell(190, 5, txt=f"{street} {number}", border=0, ln=1, align="L")
    pdf.cell(190, 5, txt=f"{zipcode} {city}", border=0, ln=1, align="L")
    pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')

    # date
    pdf.cell(190, 5, txt=str(datetime.date.today()), border=0, ln=1, align="R")
    pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')

    # bate_Number
    pdf.cell(190, 5, txt=f"Rechnungsnummer: Re-{company.bate_number}", border=0, ln=1, align="R")
    pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')

    # title
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(190, 5, txt="Rechnung", border=0, ln=1, align="L")
    pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')

    # setting header
    pdf.set_font("Arial", "B", size=13)
    for each in header:
        pdf.cell(each[1], 5, txt=each[0], border=0, ln=0, align="C")
    pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')

    # add bookings
    pdf.set_font("Arial", size=12)
    price = 0.0
    order_backup = OrderBackUp.get_by_cart_id(order.cart_id)
    voucher = None
    if order_backup and order_backup.voucher:
        voucher = Voucher.get_voucher_by_code(order_backup.voucher, order.user_id)
    for index, booking in enumerate(bookings):
        pdf.cell(31.5, 5, txt=booking.item.item_subtype.name, border=0, ln=0, align="C")
        pdf.cell(31.5, 5, txt=booking.location.name, border=0, ln=0, align="C")
        if booking.item.item_type.show_time_picker == True:
            pdf.cell(36.5, 5, txt=str(booking.start_time), border=0, ln=0, align="C")
            pdf.cell(36.5, 5, txt=str(booking.end_time), border=0, ln=0, align="C")
        else:
            pdf.cell(36.5, 5, txt=str(booking.start_time.date()), border=0, ln=0, align="C")
            pdf.cell(36.5, 5, txt=str(booking.end_time.date()), border=0, ln=0, align="C")
        tax_str = ""
        if booking.item.item_subtype.itemSubTypeTaxs:
            tax_str = ",".join(
                [f"{each.tax.name}({each.tax.percentage}%)" for each in booking.item.item_subtype.itemSubTypeTaxs])
        pdf.cell(36.5, 5, txt=tax_str, border=0, ln=0, align="C")
        pdf.cell(15.5, 5, txt=f'{booking.cost} {chr(128)}', border=0, ln=0, align="C")
        price += booking.cost

        pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')
    pdf.cell(0, h=10, txt='', border=0, ln=1, align='C')

    # price calculations
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(190, 5, txt=f"Nettosumme {round(price, 2)} {chr(128)}", border=0, ln=1, align="L")
    pdf.cell(0, h=10, txt='', border=0, ln=1, align='C')
    com_taxs = get_booking_taxs(bookings)
    for each in com_taxs:
        pdf.cell(190, 5, txt=f"{each[0]}({each[1]}%) {round(com_taxs[each], 2)}", border=0, ln=1, align="L")
        pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')
    if voucher:
        pdf.cell(190, 5, txt=f"Ermäßigt {round(voucher.price_factor / 100 * price, 2)} {chr(128)}", border=0, ln=1,
                 align="L")
        pdf.cell(0, h=5, txt='', border=0, ln=1, align='C')
        pdf.cell(190, 5, txt=f"Gesamtsumme {round(voucher.price_factor / 100 * price, 2)} {chr(128)}", border=0, ln=1,
                 align="L")
        # extra space
        pdf.cell(0, h=30, txt='', border=0, ln=1, align='C')

    else:
        pdf.cell(190, 5, txt=f"Gesamtsumme {round(price, 2)} {chr(128)}", border=0, ln=1, align="L")
        # extra space
        pdf.cell(0, h=30, txt='', border=0, ln=1, align='C')

    # ending note
    pdf.set_font("Arial", size=16)
    pdf.cell(190, 5, txt="Der Betrag ist bereits beglichen.", border=0, ln=1, align="L")

    # footer
    y_axis = pdf.get_y()  # 235
    pdf.set_font("Arial", size=13)
    if y_axis < 230:
        # 40 ki gunjaish hay
        add_space = 230 - y_axis

        pdf.cell(0, h=15 + add_space, txt='', border=0, ln=1, align='C')
        pdf.cell(190, h=5, txt=company.name, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=f'{company.street} {company.street_number} , {company.zipcode}, {company.city}',
                 border=0,
                 ln=1, align='L')
        pdf.cell(190, h=5, txt=company.commercial_registered_number, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=company.legal_representative, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=company.email_for_taxs, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=company.company_tax_number, border=0, ln=1, align='L')
    else:
        pdf.cell(0, h=10, txt='', border=0, ln=1, align='C')
        pdf.cell(190, h=5, txt=company.name, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=f'{company.street} {company.street_number} , {company.zipcode}, {company.city}',
                 border=0,
                 ln=1, align='L')
        pdf.cell(190, h=5, txt=company.commercial_registered_number, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=company.legal_representative, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=company.email_for_taxs, border=0, ln=1, align='L')
        pdf.cell(190, h=5, txt=company.company_tax_number, border=0, ln=1, align='L')
    pdf_name = f'{company.name}-Invoice-Re{company.bate_number}.pdf'
    Company.update(company.id, {"bate_number": company.bate_number + 1})
    return pdf.output(f"Invoice-{len(bookings)}.pdf", dest="S"), pdf_name
    #


def create_email(order, session=None):
    actual_text = ""
    email_text = EmailText.get_by_user_id(order.user_id, session)
    custom_values_dict = {}
    item_types_in_order = [each.booking.item.item_type.name for each in order.order_bookings]

    custom_values = [x.custom_data for x in order.order_custom_data]
    for each in custom_values:
        custom_values_dict[each.name] = each.value

    if email_text:
        actual_text = email_text.text
        custom_variables = [t for t in actual_text.split() if t.startswith('$')]
        itemType_text_variables = [t for t in actual_text.split() if t.startswith('#')]
        for each in itemType_text_variables:
            if each[1:] and each[1:] in item_types_in_order:
                item_type = ItemType.get_by_item_type_name(each[1:], session)
                if item_type and item_type.itemTypeTexts:
                    data = item_type.itemTypeTexts[0].text
                    actual_text = actual_text.replace(each, data)
                else:
                    actual_text = actual_text.replace(each, "")
            else:
                actual_text = actual_text.replace(each, "")
        actual_text = actual_text.replace("$name", order.client_name)
        for each in custom_variables:
            if each[1:] in custom_values_dict.keys():
                actual_text = actual_text.replace(each, custom_values_dict.get(each[1:]))
            else:
                actual_text = actual_text.replace(each, "")
    actual_text = actual_text.replace('\n', '<br>')
    return actual_text


def create_pdf_and_send_email(order, session=None):
    bookings = [order_booking.booking for order_booking in order.order_bookings]
    data = {}
    for booking in bookings:
        item_subtype = booking.item.item_subtype
        if item_subtype.company:
            if item_subtype.company.id not in data.keys():
                data[item_subtype.company.id] = []
            data[item_subtype.company.id].append((item_subtype, booking))

    pdfs = []
    app_configs = FrontEndCofigs.get_by_user_id(order.user_id, session)
    companies = []
    for each in data.keys():
        company = Company.query_by_id(each, session)
        bookings = [record[1] for record in data.get(each)]
        pdf = get_pdf(company, bookings, order)
        pdfs.append(pdf)
        if company.email:
            try:
                send_pdf_email(company.email, f"Rechnung - Re{company.bate_number - 1}", [pdf], app_configs.email,
                               app_configs.email_password, company)
                companies.append(company)
            except Exception as e:
                logging.exception(e)
    if len(companies) == 1:
        send_pdf_email(order.client_email, "Invoice For Order", pdfs, app_configs.email,
                       app_configs.email_password, companies[0])
    else:
        send_pdf_email(order.client_email, "Invoice For Order", pdfs, app_configs.email,
                       app_configs.email_password)