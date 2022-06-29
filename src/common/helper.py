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
                data[(tax.name, tax.percentage)] += (tax.percentage / 100) * booking.cost_without_tax
    return data


def create_pdf_and_send_email(bookings):
    data = {}
    for booking in bookings:
        item_type_id = booking.item.item_subtype_id
        if item_type_id not in data.keys():
            data[item_type_id] = []
        data[item_type_id].append(booking.id)
