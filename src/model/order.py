import datetime
import logging
from pathlib import Path

import jinja2
from fpdf import FPDF
from sqlalchemy import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Float, Integer, String

from common.email_service import send_email, send_pdf_email
# from common.helper import create_pdf_and_send_email
from configuration import configs
from model.associate_email import AssociateEmail
from model.base import Base, db
from model.booking import Booking
from model.booking_status import BookingStatus
from model.company import Company
from model.email_text import EmailText
from model.front_end_configs import FrontEndCofigs
from model.item import Item
from model.item_type import ItemType
from model.order_backup import OrderBackUp
from model.order_bookings import OrderBookings
from model.order_status import OrderStatus
from model.voucher import Voucher
from service.stripe_service import Stripe

TEMPLATE_PATH = str(Path(__file__).parent.parent) + "/templates"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader([TEMPLATE_PATH, "../templates/"]),
    autoescape=jinja2.select_autoescape(),
)


def get_pdf(company, bookings, order, session=None):
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

    app_configs = FrontEndCofigs.get_by_user_id(order.user_id, session)
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
    order_backup = OrderBackUp.get_by_cart_id(order.cart_id, session)
    voucher = None
    if order_backup and order_backup.voucher:
        voucher = Voucher.get_voucher_by_code(order_backup.voucher, order.user_id, session)
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
    com_taxs = get_booking_taxs_in_order(bookings)
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
    Company.update(company.id, {"bate_number": company.bate_number + 1}, session)
    return pdf.output(f"Invoice-{len(bookings)}.pdf", dest="S"), pdf_name
    #


def create_pdf_and_send_email_in_order(order, session=None):
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
        pdf = get_pdf(company, bookings, order, session)
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


def get_booking_taxs_in_order(bookings):
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


class Order(Base, db.Model):
    __tablename__ = "order"
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    total_cost = Column(Float, nullable=False)
    actual_total_cost = Column(Float, nullable=False)
    effected_total_cost = Column(Float, nullable=False)
    tax_amount = Column(Float, nullable=False)
    cart_id = Column(Integer, ForeignKey("cart.id", ondelete="SET NULL"), nullable=True)
    order_status_id = Column(Integer, ForeignKey("order_status.id", ondelete="SET NULL"), nullable=True)
    order_bookings = relationship("OrderBookings", backref="order")
    order_custom_data = relationship("OrderCustomData", backref="order")
    is_deleted = db.Column(db.Boolean, nullable=False, server_default=text("False"))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL"), nullable=False, index=True)

    def __init__(self, client_name, client_email, phone_number, order_status_id, total_cost, cart_id, actual_total_cost,
                 effected_total_cost, tax_amount, user_id):
        self.client_name = client_name
        self.client_email = client_email
        self.phone_number = phone_number
        self.order_status_id = order_status_id
        self.total_cost = total_cost
        self.cart_id = cart_id
        self.actual_total_cost = actual_total_cost
        self.effected_total_cost = effected_total_cost
        self.tax_amount = tax_amount
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @classmethod
    def delete(cls, id):
        cls.query.filter(cls.id == id).delete()
        db.session.commit()

    @classmethod
    def soft_delete(cls, id):
        db.session.query(cls).filter(cls.id == id).update({"is_deleted": True})
        db.session.commit()

    @classmethod
    def update(cls, id, data, session=None):

        if not session:
            session = db.session
        session.query(cls).filter(cls.id == id).update(data)
        session.commit()

    @classmethod
    def getQuery_OrderByItemType(cls, item_type_id):
        orders = db.session.query(Order).join(OrderBookings).join(Booking).filter(
            OrderBookings.booking_id == Booking.id).join(
            Item).filter(Item.item_type_id == item_type_id).group_by(Order)
        return orders

    @classmethod
    def get_order_by_cart_id(cls, cart_id):
        return cls.query.filter(cls.cart_id == cart_id).all()

    @classmethod
    def getQuery_OrderByItemSubType(cls, item_subtype_id):
        orders = db.session.query(Order).join(OrderBookings).join(Booking).filter(
            OrderBookings.booking_id == Booking.id).join(
            Item).filter(Item.item_subtype_id == item_subtype_id).group_by(Order)
        return orders

    @classmethod
    def get_pending_order_and_mark_complete(cls, session=None):
        if not session:
            session = db.session
        payment_pending_id = OrderStatus.get_id_by_name("Payment Pending", session)
        orders = session.query(cls).filter(cls.order_status_id == payment_pending_id).all()
        for each in orders:
            order_backup = OrderBackUp.get_by_cart_id(each.cart_id, session)
            if order_backup and order_backup.paypal_method and order_backup.paypal_method == "Stripe":
                resp = Stripe.retrieve_session(order_backup.payment_reference)
                if resp["payment_status"] == 'paid':
                    # process_order_completion_from_order(each, "de", order_backup.id, order_backup.voucher_code, session)
                    language = "de"
                    order_backup_id = order_backup.id

                    voucher_code = order_backup.voucher
                    order_backup = OrderBackUp.query_by_id(order_backup_id, session)
                    ## Email Text thing
                    actual_text = ""
                    email_text = EmailText.get_by_user_id(each.user_id, session)
                    custom_values_dict = {}
                    item_types_in_order = [each.booking.item.item_type.name for each in each.order_bookings]

                    custom_values = [x.custom_data for x in each.order_custom_data]
                    for custom_value in custom_values:
                        custom_values_dict[custom_value.name] = custom_value.value

                    if email_text:
                        actual_text = email_text.text
                        custom_variables = [t for t in actual_text.split() if t.startswith('$')]
                        itemType_text_variables = [t for t in actual_text.split() if t.startswith('#')]
                        for variable in itemType_text_variables:
                            if variable[1:] and variable[1:] in item_types_in_order:
                                item_type = ItemType.get_by_item_type_name(variable[1:], session)
                                if item_type and item_type.itemTypeTexts:
                                    data = item_type.itemTypeTexts[0].text
                                    actual_text = actual_text.replace(variable, data)
                                else:
                                    actual_text = actual_text.replace(variable, "")
                            else:
                                actual_text = actual_text.replace(variable, "")
                        actual_text = actual_text.replace("$name", each.client_name)
                        for variable in custom_variables:
                            if variable[1:] in custom_values_dict.keys():
                                actual_text = actual_text.replace(variable, custom_values_dict.get(variable[1:]))
                            else:
                                actual_text = actual_text.replace(variable, "")
                    actual_text = actual_text.replace('\n', '<br>')
                    #
                    email_text = actual_text
                    order_status_paid_id = OrderStatus.get_id_by_name("Paid", session)
                    if voucher_code:
                        voucher = Voucher.get_voucher_by_code(voucher_code, each.user_id, session)
                        if voucher:
                            if not voucher.counter:
                                Voucher.update(voucher.id, {"counter": 0})
                            Voucher.update(voucher.id, {"counter": voucher.counter + 1}, session)
                    tax_consumed = get_booking_taxs_in_order([each.booking for each in each.order_bookings])
                    tax_response = []
                    app_configs = FrontEndCofigs.get_by_user_id(each.user_id, session)
                    FE_URL = app_configs.front_end_url
                    for tex in tax_consumed.keys():
                        entry = {"tax_name": f'{tex[0]} ({tex[1]}%)', "tax_amount": f'{round(tax_consumed[tex], 2)}'}
                        tax_response.append(entry)
                    if language == "de":
                        associate_receipt_template = "associate_receipt_de.html"
                        receipt_template = "receipt_de.html"
                    elif language == "en":
                        associate_receipt_template = "associate_receipt_en.html"
                        receipt_template = "receipt_en.html"
                    else:
                        associate_receipt_template = "associate_receipt_en.html"
                        receipt_template = "receipt_en.html"
                    cls.update(each.id, {"order_status_id": order_status_paid_id}, session)
                    active_booking_status = BookingStatus.get_id_by_name("Active", session)

                    for booki in each.order_bookings:
                        booki.booking.update(booki.booking.id, {"booking_status_id": active_booking_status}, session)
                    try:

                        template = env.get_template(receipt_template)

                        stuff_to_render = template.render(
                            configs=configs,
                            actual_total_price=each.actual_total_cost,
                            effected_total_price=each.effected_total_cost,
                            order=each,
                            total=each.total_cost,
                            tax_amount=each.tax_amount,
                            edit_unique_key=order_backup.unique_key,
                            fe_url=FE_URL,
                            email_text=email_text,
                            footer_email=app_configs.email,
                            tax_response=tax_response
                        )

                        send_email(each.client_email, "Order Confirmation", stuff_to_render, app_configs.email,
                                   app_configs.email_password)
                        emails = AssociateEmail.getall(each.user_id, session)
                        bookings_to_check = [x.booking for x in each.order_bookings]
                        association_data = {}
                        for _email in emails:
                            item_subtypes = [x.item_subtype for x in _email.associate_email_subtypes]
                            for booking in bookings_to_check:
                                if booking.item.item_subtype in item_subtypes:
                                    if _email.email not in association_data.keys():
                                        association_data[_email.email] = []
                                    association_data[_email.email].append(booking)
                        template2 = env.get_template(associate_receipt_template)
                        for email in association_data.keys():
                            stuff_to_render2 = template2.render(
                                order_id=each.id,
                                configs=configs,
                                bookings=association_data[email],
                                footer_email=app_configs.email
                            )
                            send_email(email, "Order Confirmation for Associations", stuff_to_render2,
                                       app_configs.email,
                                       app_configs.email_password)
                    except Exception as e:
                        logging.exception(e)
                        logging.error(f"Sending Emails Failed for Order Id{each.id}")
                    # create_pdf_and_send_email(each)

    @classmethod
    def get_completed_order_and_mark_complete(cls, session=None):
        if not session:
            session = db.session
        paid_id = OrderStatus.get_id_by_name("Paid", session)
        completed_id = OrderStatus.get_id_by_name("Completed", session)
        orders = session.query(cls).filter(cls.order_status_id == paid_id).all()
        for order in orders:
            completed = True
            for each in order.order_bookings:
                if each.booking.end_time > datetime.datetime.now():
                    completed = False
                Booking.close_booking(each.booking.id, session)
            if completed:
                create_pdf_and_send_email_in_order(order, session)
                cls.update(order.id, {"order_status_id": completed_id}, session)
