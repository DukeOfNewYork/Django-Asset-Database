from django.http import HttpResponse
import csv


def format_csv(data, file_name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '.csv"'
    writer = csv.writer(response)
    writer.writerow(["Location","Name","Room","Date","1"])
    for x in data:
        writer.writerow([x.location,x.name, x.room, ("{:%Y-%m-%d %H:%M}".format(x.pub_date))])
    return response
