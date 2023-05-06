import time

import requests
from academic_plans.models import AcademicPlan, EducationalProgram, FieldOfStudy
from django.db import transaction
from tasks.models import Subject, SubjectInAcademicPlan

host = "https://op.itmo.ru/"


def get_academic_plan_ids() -> list[int]:
    page = 1
    academic_plan_ids = []
    while True:
        resp = requests.get(
            f"{host}api/academicplan?page={page}",
            headers={"Accept": "application/json"},
        ).json()
        for academic_plan in resp["results"]:
            if academic_plan["id"] not in academic_plan_ids:
                academic_plan_ids.append(academic_plan["id"])
        if resp["next"] is not None:
            page += 1
        else:
            break
    return academic_plan_ids


def parse_field_of_study(data: dict) -> FieldOfStudy:
    id = data["id"]
    title = data["title"]
    number = data["number"]
    field_of_study, _ = FieldOfStudy.objects.get_or_create(
        id=id, title=title, number=number
    )
    return field_of_study


def parse_educational_program(data: dict) -> EducationalProgram:
    id = data["id"]
    enrollment_year = data["year"]
    title = data["title"]
    educational_program, _ = EducationalProgram.objects.get_or_create(
        id=id,
        enrollment_year=enrollment_year,
        title=title,
    )

    for field_of_study_data in data["field_of_study"]:
        field_of_study = parse_field_of_study(field_of_study_data)
        educational_program.fields_of_study.add(field_of_study)

    return educational_program


def get_semesters(ze_v_sem: str) -> list[int]:
    ze_lst = ze_v_sem.split(", ")
    semesters = []
    for i in range(len(ze_lst)):
        if ze_lst[i] != "0":
            semesters.append(i)
    return semesters


def parse_subjects(data, academic_plan):
    for block in data:
        modules = block["modules_in_discipline_block"]
        for module in modules:
            blocks_in_module = module["change_blocks_of_work_programs_in_modules"]
            for block_in_module in blocks_in_module:
                subjects = block_in_module["work_program"]
                for subject in subjects:
                    if not subject["ze_v_sem"]:
                        continue
                    id = subject["id"]
                    title = subject["title"]
                    semesters = get_semesters(subject["ze_v_sem"])
                    subject, _ = Subject.objects.get_or_create(
                        id=id,
                        title=title,
                    )

                    SubjectInAcademicPlan.objects.get_or_create(
                        subject=subject,
                        semesters=semesters,
                        academic_plan=academic_plan,
                    )


def parse_academic_plan(id: int):
    resp = requests.get(
        f"{host}api/academicplan/detail/{id}",
        headers={"Accept": "application/json"},
        timeout=5,
    ).json()

    if int(resp["academic_plan_in_field_of_study"][0]["year"]) < 2019:
        return
    educational_program = parse_educational_program(
        resp["academic_plan_in_field_of_study"][0]
    )

    academic_plan, _ = AcademicPlan.objects.get_or_create(
        educational_program=educational_program
    )

    parse_subjects(resp["discipline_blocks_in_academic_plan"], academic_plan)


def parse_data() -> None:
    academic_plan_ids = get_academic_plan_ids()
    with transaction.atomic():
        for academic_plan_id in academic_plan_ids:
            print("Parsing ", academic_plan_id)
            try:
                parse_academic_plan(academic_plan_id)
            except Exception as exc:
                print(str(exc))
            time.sleep(1)


def test_parse_data(id):
    with transaction.atomic():
        parse_academic_plan(id)
