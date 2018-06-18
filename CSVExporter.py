import csv

from Exporter import Exporter


class CSVExporter(Exporter):

    def write(records, filename):
        print("Writing records to csv", len(records))
        print(filename)

        with open(filename, "w", newline='') as csvFile:
            # fields = ['Id', 'Name', 'Username', 'Email', 'Repositories', 'Stars', 'Followers', 'Following']
            fields = records[0].variables.keys()
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            index = 0
            for record in records:
                writer.writerow(record.variables)
                # writer.writerow({index.__add__(1), record.variables})
        print("Writing finished")


if __name__ == '__main__':
    from User import User
    user = User()
    user.set('username', 'Abhi2@gh')
    user.set('name', 'Abhijit2')
    user.set('email', "ab2@cd.com")
    users = [user, user]
    p = "C:\\Users\\abhijit.patil\\PycharmProjects"
    # print(p)
    # now = datetime.datetime.now()
    # str = now.strftime("%Y-%m-%d_%H%M")
    filename = "{}\{}_{}.csv".format(p, "gh_users", "")
    exporter = CSVExporter
    exporter.write(records=users, filename=filename)
