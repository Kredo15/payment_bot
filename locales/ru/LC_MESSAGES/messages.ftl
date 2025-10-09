hello =
    <b>Вы находитесь в главном меню</b>

    <b>Тарифные планы</b> - оплатить подписку
    <b>Моя подписка</b> - текущая подписка
    <b>Профиль</b> - настройки профиля
    <b>Поддержка</b> - написать в поддержку

profile_message =
    👤 Профиль

    — Telegram ID: <i>{ $telegram_id }</i>
    — Ваш текущий язык: 🇷🇺 <i>Русский</i>
    — Часовой пояс: <i>{ $time_zone }</i>
    — Почта: <i>{ $email }</i>
    Здесь можно настраивать свой аккаунт:

my_subscription_message =
    🔑 Моя подписка

tariff_message =
    💳 Тарифные планы

    Продукт: Закрытый канал

support_message =
    🤝 Поддержка

    💌 По всем вопросам пишите @support_bot

choose_language =
    👤 Профиль

    📝 Редактирование языка

    Выберите язык бота:

subscription_message =
    Продукт: Закрытый канал

    Тарифный план: { $name }

    - <i>Период</i>: { $duration_days } дней
    - <i>Цена</i>: { $price } { $currency }

payment_method =
    Продукт: Закрытый канал

    Тарифный план: { $name }

    Выберите способ оплаты:

public_offer =
    Продукт: Закрытый канал

    Тарифный план: { $name }

    - <i>Период</i>: { $duration_days } дней
    - <i>Цена</i>: { $price } { $currency }

    ℹ️ Оплачивая подписку, Вы принимаете условия Публичной оферты (https://disk.yandex.ru/i/X_EiWe_5Be6CNA).

email_request =
    Продукт: Закрытый канал

    Тарифный план: { $name }

    Введите E-mail:

en_lang = English
ru_lang = Русский
lang_is_switched = Язык переключен на { ru_lang }.

success_payment =
    ✅ Оплата прошла успешно!

    Вы получили доступ к закрытому каналу "[Название канала]".

    Подписка действует до: { $end_date }

failed_payment =
    ❌ Оплата не удалась. ❌

    Если у вас возникли трудности, наша служба поддержки готова помочь: @support_bot

#Кнопки
tariff_button = 💳 Тарифные планы
profile_button = 👤 Профиль
subscription_button = 🔑 Моя подписка
support_button = 🤝 Поддержка
admin_button = ⚙️ Админ панель

language_button = 🌍 Язык
email_button = 📬 Почта
time_zone_button = 🌐 Часовой пояс

subscription = Подписка | { $duration_days } дней | { $price } { $currency }

pay = 💳 Оплатить
yookassa = ЮMoney
crypt = 🏳️️ Крипта
to_payment = 💰 Перейти к оплате
back = ← Назад