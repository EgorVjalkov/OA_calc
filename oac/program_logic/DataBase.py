import csv
from data import patient_file_questionnaire
from Menu import Menu


class DataBase:
    def __init__(self):
        self.temp_database_count = 0
        self.head = []
        self.db = {}
        self.database_path = '../patients/patients.csv'

    def open_db(self, behavior=''):
        if behavior == 'temp_db':
            self.temp_database_count += 1
            self.database_path = f'patients/temp_database_{self.temp_database_count}.csv'

        open(self.database_path, 'a').close() # создаем пустой файл если нужно

        with open(self.database_path, 'r') as db:
            self.db = list(csv.DictReader(db, delimiter=','))

            if not self.db:
                self.head = []
            else:
                self.head = list(self.db[0].keys())
        #print(self.head)

        return self.db, self.head, self.database_path

    def is_head_matched_or_empty(self, head):
        flag = True if head == self.head or not self.head else False
        #print(head is self.head, self.head)
        return flag

    def get_patients_with_missing_data(self):
        patients_with_missing_data = {}
        for i in self.db:
            if None in i.values():
                patient_id = f"{i['datetime']} - {i['name']}"
                patients_with_missing_data[patient_id] = i
        return patients_with_missing_data

    def change_patient_with_missing_data_and_get_index(self, patients_with_missing_data):
        if not patients_with_missing_data:
            return False
        else:
            menu = Menu(topic='Change a patient', variants=list(patients_with_missing_data.keys()))
            menu.print_a_topic()
            menu.print_variants()
            changed_patient_id = menu.get_user_answer()
            return patients_with_missing_data[changed_patient_id]

    def answer_the_questionnaire(self, questionnaire):
        answers_dict = {}
        try:
            for question in questionnaire:
                variants_of_answer = questionnaire[question]
                menu = Menu(question, variants_of_answer)
                menu.print_a_topic()
                if variants_of_answer:
                    menu.print_variants()
                answers_dict[question] = menu.get_user_answer()
        except KeyboardInterrupt:
            print()
            return answers_dict
        return answers_dict

    def write_patient_data_to_default_db(self, patient_data={}, behavior='new', questionnaire_flag=False):
        if behavior == 'new':
            head_of_frame = list(patient_data.keys()) + list(patient_file_questionnaire)
            self.open_db()
            while True:
                if self.is_head_matched_or_empty(head_of_frame):
                    print(f'данные будут размещены в {self.database_path}')
                    break
                else:
                    self.open_db('temp_db')

            with open(self.database_path, 'a') as database:
                database_writer = csv.writer(database)
                if not self.head:
                    database_writer.writerow(head_of_frame)

                if questionnaire_flag:
                    if patient_data['name'] == 'noname':
                        patient_data['name'] = input('Enter patient`s name\n: ')
                    patient_answers = list(patient_data.values())
                    patient_answers.extend(list(self.answer_the_questionnaire(patient_file_questionnaire).values()))
                else:
                    patient_answers = list(patient_data.values())

                database_writer.writerow(patient_answers)

        elif behavior == 'add':
            self.open_db()
            missing_data = self.change_patient_with_missing_data_and_get_index(self.get_patients_with_missing_data())
            if not missing_data:
                print('You don`t have patients with missing data\n')
                return

            patient_answers = missing_data.copy()
            if patient_answers['name'] == 'noname':
                input_name = Menu(topic='Input patient`s name', variants='')
                input_name.print_a_topic()
                patient_answers['name'] = input_name.get_user_answer()

            missing_questions = [i for i in patient_answers.keys() if not patient_answers[i]]
            missing_questions = {i: data.patient_file_questionnaire[i] for i in data.patient_file_questionnaire
                                 if i in missing_questions}
            missing_questions = self.answer_the_questionnaire(missing_questions)
            patient_answers.update(missing_questions)

            def replacer(frame_row, changed_patient_row, new_row):
                if changed_patient_row == frame_row:
                    return new_row

            self.db = [replacer(row, missing_data, patient_answers) for row in self.db]
            self.db = [list(i.values()) for i in self.db]
            self.db.insert(0, self.head)

            with open(self.database_path, 'w') as database:
                database_writer = csv.writer(database)
                database_writer.writerows(self.db)

    def refactor(self):
        self.head = self.db['datetime name']
        self.write_patient_data_to_default_db(behavior='add')
        # здесь сложно. нужно отработать через дикт райтер как таблицу


db = DataBase()
db.open_db()
db.write_patient_data_to_default_db(behavior='add')
