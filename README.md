# AIKryptoBot3 - Autonomous Cryptocurrency Trading Bot

## Översikt
AIKryptoBot3 är en helt självgående kryptovalutahandelsbot som använder adaptiva maskininlärningsalgoritmer för att maximera vinst på Kraken-börsen. Systemet kör dygnet runt utan manuell intervention.

## ⚠️ VIKTIGA SÄKERHETSVARNINGAR
- **ANVÄND PÅ EGEN RISK**: Automatisk handel kan resultera i betydande förluster
- **BÖRJA SMÅTT**: Testa med små belopp först
- **ÖVERVAKA REGELBUNDET**: Kontrollera systemets prestanda dagligen
- **SÄKERHETSKOPIERA**: Håll alltid backup på konfigurationsfiler

## Funktioner
- 🤖 Helt automatisk handel utan manuella bekräftelser
- 📊 Adaptiva algoritmer som lär sig från tidigare trades
- 🔄 Automatisk loggrensning för att undvika stora filer
- 📱 Telegram-notifikationer för alla trades
- ⏰ Dynamisk schemaläggning (15-60 min intervall)
- 🛡️ Stop-loss och riskhantering

## Installation

### Förutsättningar
- Python 3.8+
- Kraken API-nycklar
- Telegram Bot Token

### Steg 1: Klona och installera
```bash
git clone https://github.com/Emtatos/AIKryptoBot3.git
cd AIKryptoBot3
pip install -r requirements.txt
```

### Steg 2: Konfigurera API-nycklar
1. Skapa `config/kraken.key` med dina Kraken API-uppgifter:
```
[API_KEY]
[PRIVATE_KEY]
```

2. Uppdatera `config/telegram_config.py`:
```python
TELEGRAM_TOKEN = "din_bot_token"
TELEGRAM_CHAT_ID = "ditt_chat_id"
```

### Steg 3: Konfigurera handelsparametrar
Redigera `config/config.py`:
- `CAPITAL_ALLOC_PCT`: Andel av saldo att använda (1.0 = 100%)
- `MIN_SELL_VALUE`: Minsta försäljningsvärde i USD
- `ACTIVE_COINS`: Lista över kryptovalutor att handla

## Användning

### Starta automatisk handel
```bash
python scheduler/dynamic_scheduler.py
```

### Engångskörning (för testning)
```bash
python start_all.py
```

### Övervaka loggar
```bash
tail -f logs/signal_log.csv
tail -f logs/buy_log.csv
tail -f logs/sell_log.csv
```

## Systemarkitektur

### Kärnkomponenter
- `core/momentum_generator.py`: Beräknar teknisk analys
- `core/broker_kraken.py`: Kraken API-integration
- `tools/recommendation_engine.py`: Handelsbeslut och exekvering
- `scheduler/dynamic_scheduler.py`: Kontinuerlig körning

### Adaptiva algoritmer
- `core/adaptive_buy_score.py`: Justerar köptrösklar baserat på träffsäkerhet
- `core/adaptive_switch_threshold.py`: Optimerar växlingslogik
- `core/log_rotator.py`: Automatisk filhantering

### Dataflöde
```
Livepris → Momentum → Adaptiva algoritmer → Handelsbeslut → Automatisk exekvering → Telegram-notifiering
```

## Säkerhet och riskhantering

### Inbyggda säkerhetsmekanismer
- Stop-loss på alla positioner
- Maximal kapitalallokering per trade
- Minsta handelsvolym-gränser
- Automatisk felhantering

### Rekommenderade övervakningsrutiner
1. **Daglig kontroll**: Granska Telegram-meddelanden
2. **Veckovis**: Analysera `logs/signal_accuracy.csv`
3. **Månadsvis**: Utvärdera total prestanda

## Felsökning

### Vanliga problem
- **"Kraken API-fel"**: Kontrollera API-nycklar och internetanslutning
- **"Otillräckligt saldo"**: Justera `CAPITAL_ALLOC_PCT` eller lägg till mer USD
- **"Telegram-fel"**: Verifiera bot-token och chat-ID

### Loggar att kontrollera
- `logs/signal_log.csv`: Handelssignaler
- `logs/signal_accuracy.csv`: Algoritmens prestanda
- `logs/threshold_history.csv`: Adaptiva justeringar

## Avancerad konfiguration

### Anpassa handelsintervall
Redigera `scheduler/dynamic_scheduler.py`:
```python
def get_interval():
    # Anpassa tider och intervall efter behov
    if 8 <= hour < 22:
        return 10  # Mer frekvent handel
```

### Lägg till nya kryptovalutor
1. Uppdatera `config/coin_config.py`
2. Kontrollera att Kraken stödjer paret
3. Testa med små belopp först

## Support och utveckling
- GitHub Issues: Rapportera buggar och föreslå funktioner
- Telegram: Följ bot-loggarna för realtidsuppdateringar

## Licens
Använd på egen risk. Utvecklaren tar inget ansvar för handelsförluster.
