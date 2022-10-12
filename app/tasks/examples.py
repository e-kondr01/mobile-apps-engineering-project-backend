TASK_DATE_GROUPS_RESPONSE_EXAMPLE = {
    "No deadline": [
        {
            "id": 4,
            "title": "Тестовое задание без дедлайна",
            "subject": {
                "id": 1,
                "title": "Проектирование мобильных и сетевых приложений",
            },
            "deadline_at": None,
            "is_urgent": False,
            "is_overdue": False,
        }
    ],
    "2022-10-11": [
        {
            "id": 3,
            "title": "Тест создания",
            "subject": {"id": 2, "title": "Аааа"},
            "deadline_at": "2022-10-11T03:00:00+03:00",
            "is_urgent": False,
            "is_overdue": True,
        }
    ],
    "2022-10-26": [
        {
            "id": 2,
            "title": "Выбор группы",
            "subject": {
                "id": 1,
                "title": "Проектирование мобильных и сетевых приложений",
            },
            "deadline_at": "2022-10-26T03:00:00+03:00",
            "is_urgent": True,
            "is_overdue": False,
        },
        {
            "id": 5,
            "title": "Тестовое 2",
            "subject": {
                "id": 1,
                "title": "Проектирование мобильных и сетевых приложений",
            },
            "deadline_at": "2022-10-26T19:43:36+03:00",
            "is_urgent": True,
            "is_overdue": False,
        },
    ],
    "2022-12-31": [
        {
            "id": 1,
            "title": "Проект",
            "subject": {
                "id": 1,
                "title": "Проектирование мобильных и сетевых приложений",
            },
            "deadline_at": "2022-12-31T03:00:00+03:00",
            "is_urgent": False,
            "is_overdue": False,
        }
    ],
}
