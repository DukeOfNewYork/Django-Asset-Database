from django.http import HttpResponse
import csv


def format_csv(data, file_name):
    last_loc = ""
    last_room = ""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + file_name + '.csv"'
    writer = csv.writer(response)
    writer.writerow([file_name])
    for x in data:
        if last_loc != x.location:
            last_loc = x.location
            writer.writerow([""])
            writer.writerow([""])
            writer.writerow([x.location])
        elif last_room != x.room:
            last_room = x.room
            writer.writerow([""])
        writer.writerow([x.name, x.room, ("{:%Y-%m-%d %H:%M}".format(x.pub_date))])
    return response
