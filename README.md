# Application Notifier

## Описание
Данный сервис служит интеграцией Zulip и Кабинет МИЭМ, позволяя настроить отправку сообщений в определённый топик чата при подаче заявок на вакансию в заданный проект в кабинете.

## Использование
- Для добавления проекта под контроль требуется отправить `POST` на `/subscription/{slug}/{stream}/{topic}`, где `slug` - номер проекта в кабинете, `stream` - название канала в zulip, `topic` - для отправки сообщений.
- Для остановки контроля требуется отправить `DELETE` на `/subscription/{slug}`, где `slug` - номер проекта в кабинете.

## Деплой
Развёртка осуществляется с помощью Docker:
1. Откройте docker-compose.yaml и внесите настройки в разделе environment сервисов server и timer.
2. Запустите команду
```
sudo docker-compose up -d
```
3. Радуйтесь
