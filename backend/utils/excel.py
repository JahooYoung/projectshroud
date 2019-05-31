import os
import re
import openpyxl
from django.conf import settings
from backend.models import UserRegisterEvent


TEMPLATE_FILE_PATH = os.path.join(settings.FILES_DIR, 'template/Export_template.xlsx')
export_fields = {'user': ['real_name', 'mobile', 'email', 'is_activated'],
                 'status': ['approved', 'application_text'],
                 'transport': ['transport_type', 'transport_id', 'depart_station', 'depart_time',
                               'arrival_station', 'arrival_time', 'other_detail']
                }


def fillrow(sheet, row, require_approve, ure):
    user = ure.user
    transport = ure.transport
    col = 1
    for field in export_fields['user']:
        sheet.cell(row=row, column=col).value = getattr(user, field)
        col += 1
    if require_approve:
        if ure.approved:
            sheet.cell(row=row, column=col).value = '审核通过'
        else:
            sheet.cell(row=row, column=col).value = '审核中'
            col += 1
            sheet.cell(row=row, column=col).value = ure.application_text
        col += 1
    else:
        if ure.approved:
            sheet.cell(row=row, column=col).value = '已注册'
        col += 1

    if transport is not None:
        for field in export_fields['transport']:
            sheet.cell(row=row, column=col).value = getattr(transport, field)
            col += 1

    return 1


def export(event):
    ure_list = UserRegisterEvent.objects.filter(event=event)
    file = openpyxl.load_workbook(TEMPLATE_FILE_PATH)

    sheet1 = file['已注册参会者']
    sheet2 = file['申请参会者']

    row1 = 3
    row2 = 3

    for ure in ure_list:
        col = 0
        if ure.approved:
            row1 += fillrow(sheet1, row1, event.require_approve, ure)
        else:
            row2 += fillrow(sheet2, row2, event.require_approve, ure)

    row1 += 1
    sheet1.cell(row=row1, column=1).value = '总人数:'
    sheet1.cell(row=row1, column=2).value = row1 - 4

    row2 += 1
    sheet2.cell(row=row2, column=1).value = '总人数:'
    sheet2.cell(row=row2, column=2).value = row2 - 4
    if not event.require_approve:
        del file['申请参会者']

    file_name = '%s_参会信息.xlsx' % re.sub(r'[\s]+', '-', event.title)
    file_path = os.path.join(os.path.join(settings.FILES_DIR, 'temp'), file_name)
    file.save(file_path)

    return file_path, file_name

