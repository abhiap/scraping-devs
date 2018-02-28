import csv
import configparser

from User import User


class Exporter:

    @staticmethod
    def write_to_csv(records):
        print("Writing records to csv", len(records))
        config = configparser.ConfigParser()
        config.read('config.ini')
        filename = config['DEFAULT']['export_folder_path']
        print(filename)
        filename = filename.__add__("gh_users.csv")
        print(filename)

        with open(filename, "w", newline='') as csvFile:
            fields = ['Id', 'Name', 'Username', 'Email', 'Repositories', 'Stars', 'Followers', 'Following']
            writer = csv.DictWriter(csvFile, fieldnames=fields)
            writer.writeheader()
            index = 0
            for record in records:
                writer.writerow(record.variables)
                # writer.writerow({index.__add__(1), record.variables})
        print("Writing finished")


if __name__ == '__main__':
    user = User()
    user.set('username', 'Abhi2@gh')
    user.set('name', 'Abhijit2')
    user.set('email', "ab2@cd.com")
    users = [user, user]
    Exporter.write_to_csv(users)
