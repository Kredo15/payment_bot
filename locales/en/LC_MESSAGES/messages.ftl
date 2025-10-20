hello =
    <b>You are in the main menu</b>

    <b>Tariff plans</b> - pay for a subscription
    <b>My subscription</b> - current subscription
    <b>Profile</b> - profile settings
    <b>Support</b> - write to support

profile_message =
    👤 Profile

    — Telegram ID: <i>{ $telegram_id }</i>
    — Your current language: 🇺🇸 <i>English</i>
    — Time zone: <i>{ $time_zone }</i>
    — Email: <i>{ $email }</i>
    You can set up your account here:

subscription_message =
    🔑 My subscription

tariff_message =
    💳 Tariff plans

    Product: Private chanel

support_message =
    🤝 Support

    💌 If you have any questions, please write @support_bot

choose_language =
    👤 Profile

    📝 Language editing

    Select the language of the bot:

subscription_message =
    Product: Private chanel

    Tariff plan: { $name }

    - <i>Period</i>: { $duration_days } days
    - <i>Price</i>: { $price } { $currency }

referral_info =
        <b>🤝 Referral program</b>

        <i>Invite your friends and get bonuses!</i>

        <b>How does it work?</b>
        <b>•</b> For each guest — <b>+1 subscription day</b> and +1 to the referral counter.
        <b>•</b> The more friends you have, the higher your</b> and more privileges!
        <b>🏆 Referral levels:</b>
        <b>1 level</b> — 0 referral
        <b>2 level</b> — 1–2 referral
        <b>3 level</b> — 3–9 referral
        <b>4 level</b> — 10–29 referral
        <b>5 level</b> — 30+ referral

        <b>🚀 How can I level up?</b>
        — Just invite your friends! Progress and current level are always visible in your <b>profile</b>.

invite_friend_message =
        👥 <b>Invite a friend and get a bonus!</b>

        Send this link to your friends, and you'll get a nice bonus for each new user!

        { $ref_link }

referral_list =
    <b>Your referrals</b>

referral_all =
    All { $all } people

not_referral =
    You don't have any referrals yet. Invite your friends and get a bonus!

payment_method =
    Product: Private chanel

    Tariff plan: { $name }

    Выберите способ оплаты:

public_offer =
    Product: Private chanel

    Tariff plan: { $name }

    - <i>Period</i>: { $duration_days } days
    - <i>Price</i>: { $price } { $currency }

    ℹ️ By paying for a subscription, you accept the terms of the Public Offer (https://disk.yandex.ru/i/X_EiWe_5Be6CNA).

email_request =
    Product: Private chanel

    Tariff plan: { $name }

    Enter E-mail:

en_lang = English
ru_lang = Русский
lang_is_switched = Display language is { en_lang }.

change_email =
    📝 Editing mail

    Enter the E-mail in the format: customer@mail.ru

not_valid_email =
    Incorrect mail format

#Buttons
tariff_button = 💳 Tariff plans
profile_button = 👤 Profile
my_subscription_button = 🔑 My subscription
support_button = 🤝 Support
admin_button = ⚙️ Admin panel

referral_button = 🌐 Referral program
invite_friend = 👥 Invite a friend
my_referral_button = 📊 My referral
language_button = 🌍 Language
email_button = 📬 Email
time_zone_button = 🌐 Time zone

subscription = Subscription | { $duration_days } days | { $price } { $currency }

pay = 💳 Pay
yookassa = ЮMoney
crypt = 🏳️️ Crypt
to_payment = 💰 To payment
back = ← Back