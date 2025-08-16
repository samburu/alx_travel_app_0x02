## Run Migrations and Seed Database
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed
```

## Run the development server:
``` bash
python manage.py runserver
```

## API Endpoints

- `/api/listings/`
- `/api/bookings/`

# Chapa Payment Integration

This app integrates **Chapa Payment Gateway** for secure bookings.

### Features
- Initiate payments via `/initiate-payment/`
- Verify payments via `/verify-payment/`
- Payment status stored in DB
- Celery task sends email confirmation

### Testing
1. Set your sandbox `CHAPA_SECRET_KEY` in `.env`
2. Run Django server
3. Initiate payment with curl
4. Verify payment after checkout

