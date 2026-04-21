
## Лекция: Стратегии быстрой отладки — как находить проблемы за минуты, а не часы

### 1. Что вы сделали правильно (и что заняло много времени)

**Ваш путь к успеху:**

```
1. Бот падал с ошибкой 400 → часами смотрели логи
2. Вербозные логи были пустыми → искали причину
3. Сравнивали успешный и неудачный запросы → нашли разницу в seed
4. Исправили отправку параметров → получили 200 ✅
```

**Сколько времени заняло:** Вероятно, несколько часов или дней.

**Как сократить до 15-20 минут:** Использовать **системный подход к отладке**.

### 2. Чек-лист быстрой отладки (печатайте и вешайте над монитором)

```
┌─────────────────────────────────────────────────────────────────┐
│           10 ШАГОВ БЫСТРОЙ ОТЛАДКИ (15 минут)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  □ 1. Посмотреть HTTP статус (200? 400? 500?)                   │
│     → Если не 200, проблема есть                                │
│                                                                  │
│  □ 2. Проверить тело ответа (сервер часто пишет причину)        │
│     → В вашем случае: {"ERRORS":{"captcha":["неверно"]}}         │
│                                                                  │
│  □ 3. Сравнить успешный и неудачный запросы (diff логов)        │
│     → Искать различия в: параметрах, заголовках, cookie         │
│                                                                  │
│  □ 4. Проверить, не изменились ли входные данные                │
│     → Размер seed: 128 байт vs 96 байт                          │
│                                                                  │
│  □ 5. Включить curl verbose на время отладки                    │
│     → CURLOPT_VERBOSE=true, CURLOPT_STDERR=fopen('php://temp')  │
│                                                                  │
│  □ 6. Сохранить полный запрос и ответ в файл                    │
│     → file_put_contents('/tmp/debug.txt', $request . $response) │
│                                                                  │
│  □ 7. Повторить запрос вручную через curl в терминале           │
│     → curl -v -X POST https://... -d '...'                      │
│                                                                  │
│  □ 8. Проверить синтаксис: нет ли лишних пробелов, запятых      │
│     → captcha vs captchaInput — одна буква решает!              │
│                                                                  │
│  □ 9. Проверить порядок отправки (сессия должна быть та же)     │
│     → JSESSIONID не должен меняться между шагами                │
│                                                                  │
│  □ 10. Использовать сниффер трафика (Wireshark/tcpdump)         │
│      → Когда ничего не помогает, смотрим на уровне пакетов      │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Инструменты отладки (с примерами для вашего кейса)

#### Инструмент 1: Логирование в файл (вместо echo)

```php
// ВАШ СТАРЫЙ СПОСОБ (медленный, теряется при перезапуске)
echo "\n=== VERBOSE ===\n";
echo $verboseLog;

// НОВЫЙ СПОСОБ (быстрый, сохраняется)
$debugFile = '/tmp/curl_debug_' . date('Ymd_His') . '.log';
file_put_contents($debugFile, "=== VERBOSE ===\n" . $verboseLog, FILE_APPEND);
file_put_contents($debugFile, "=== REQUEST HEADERS ===\n" . $requestHeaders, FILE_APPEND);
file_put_contents($debugFile, "=== RESPONSE HEADERS ===\n" . $headers, FILE_APPEND);
file_put_contents($debugFile, "=== BODY ===\n" . $body, FILE_APPEND);

// Потом смотрите: cat /tmp/curl_debug_*.log
```

#### Инструмент 2: Функция-обертка для отладки

```php
function debugCurl($ch, $label = 'request') {
    $info = curl_getinfo($ch);
    
    // Быстрая диагностика за 1 секунду
    $debug = [
        'time' => date('Y-m-d H:i:s'),
        'label' => $label,
        'http_code' => $info['http_code'],
        'total_time' => $info['total_time'],
        'url' => $info['url'],
        'size_download' => $info['size_download'],
    ];
    
    // Если ошибка — логируем всё
    if ($info['http_code'] != 200) {
        $debug['error'] = curl_error($ch);
        $debug['errno'] = curl_errno($ch);
        // Получаем verbose лог
        // ...
    }
    
    file_put_contents('/tmp/curl_debug.log', json_encode($debug) . "\n", FILE_APPEND);
    return $debug;
}
```

#### Инструмент 3: Сравнение двух запросов (diff)

```bash
# Сохраняем успешный и неудачный запросы
echo "$SUCCESS_REQUEST" > /tmp/success.txt
echo "$FAILED_REQUEST" > /tmp/failed.txt

# Сравниваем (покажет различия!)
diff -u /tmp/success.txt /tmp/failed.txt

# Результат:
# -captcha=123456
# +captchaInput=123456
#   ↑ это и была проблема!
```

#### Инструмент 4: Копирование запроса из браузера в curl

```bash
# В браузере (Chrome DevTools → Network → ПКМ на запросе)
# Copy → Copy as cURL

# Получаете готовую команду:
curl 'https://service.nalog.ru/bi2-proc.json' \
  -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Cookie: JSESSIONID=...' \
  --data-raw 'requestType=FINDPRS&innPRS=2239000934&bikPRS=044525225'

# Запускаете в терминале — сразу видно, работает или нет!
```

### 4. Типичные ошибки и их быстрая диагностика

| Симптом | Что проверять в первую очередь | Команда/Действие |
|---------|-------------------------------|------------------|
| **HTTP 400** | Имена параметров | `diff` между рабочим и сломанным запросом |
| **HTTP 401** | Авторизация, токен | `echo $postParams \| grep -i "token\|auth"` |
| **HTTP 403** | Доступ, CSRF-токен | Проверить Referer и Origin заголовки |
| **HTTP 404** | URL | `echo $url` — нет ли лишних пробелов |
| **HTTP 500** | Смотреть тело ответа | Сервер часто пишет ошибку в JSON |
| **Пустой ответ** | CURLOPT_HEADER vs VERBOSE | Убрать CURLOPT_HEADER для отладки |
| **Нет соединения** | Прокси, порт, DNS | `telnet proxy_ip port` |
| **Меняется сессия** | Cookie Path | Сравнить `Set-Cookie` заголовки |

### 5. Ваш личный "Дзен отладки" (правила)

```php
// ПРАВИЛО 1: Всегда логируй ВХОДНЫЕ данные
error_log("[INPUT] POST params: " . json_encode($postParams));
error_log("[INPUT] URL: " . $url);

// ПРАВИЛО 2: Всегда логируй ВЫХОДНЫЕ данные (хотя бы статус)
error_log("[OUTPUT] HTTP " . $info['http_code'] . ", Size: " . strlen($content));

// ПРАВИЛО 3: При ошибке 4xx — логируй ВСЁ
if ($info['http_code'] >= 400 && $info['http_code'] < 500) {
    file_put_contents('/tmp/error_' . date('Ymd_His') . '.log', 
        "URL: $url\n" .
        "POST: " . print_r($postParams, true) . "\n" .
        "RESPONSE: " . $content . "\n" .
        "VERBOSE: $verboseLog\n"
    );
}

// ПРАВИЛО 4: Имей шаблон для быстрого теста в терминале
// Сохраните в файл test.sh:
#!/bin/bash
curl -v -X POST "https://service.nalog.ru/bi2-proc.json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: JSESSIONID=..." \
  --data-urlencode "requestType=FINDPRS" \
  --data-urlencode "innPRS=$1" \
  --data-urlencode "bikPRS=044525225"
```

### 6. Создание "портала отладки" (одна функция для всего)

```php
class DebugHelper {
    private static $enabled = true;
    private static $logFile = '/tmp/api_debug.log';
    
    public static function log($label, $data) {
        if (!self::$enabled) return;
        
        $entry = [
            'timestamp' => microtime(true),
            'label' => $label,
            'data' => $data,
            'memory' => memory_get_usage(),
        ];
        
        file_put_contents(
            self::$logFile,
            json_encode($entry) . "\n",
            FILE_APPEND
        );
    }
    
    public static function compare($label1, $data1, $label2, $data2) {
        echo "\n=== DIFF: $label1 vs $label2 ===\n";
        
        // Если это строки — показываем различия
        if (is_string($data1) && is_string($data2)) {
            system("diff -u <(echo '$data1') <(echo '$data2')");
        } else {
            // Если массивы — сравниваем рекурсивно
            $diff = array_diff_assoc($data1, $data2);
            print_r($diff);
        }
    }
    
    public static function curlVerbose($ch, $label) {
        $verbose = fopen('php://temp', 'w+');
        curl_setopt($ch, CURLOPT_VERBOSE, true);
        curl_setopt($ch, CURLOPT_STDERR, $verbose);
        
        $result = curl_exec($ch);
        
        rewind($verbose);
        $log = stream_get_contents($verbose);
        fclose($verbose);
        
        self::log($label . '_verbose', $log);
        
        return $result;
    }
}

// Использование:
DebugHelper::log('start_request', ['url' => $url, 'post' => $postParams]);
$content = DebugHelper::curlVerbose($ch, 'captcha_request');
DebugHelper::log('end_request', ['http_code' => $info['http_code']]);
```

### 7. Быстрый доступ к логам (алиасы в .bashrc)

```bash
# Добавьте в ~/.bashrc
alias log-curl='tail -f /tmp/curl_debug.log'
alias log-error='cat /tmp/error_*.log | tail -50'
alias log-clear='rm -f /tmp/curl_debug.log /tmp/error_*.log'
alias diff-requests='diff -u /tmp/success.txt /tmp/failed.txt'

# После добавления:
source ~/.bashrc

# Теперь просто вводите:
log-curl        # смотреть логи в реальном времени
log-error       # последние ошибки
```

---

## 3 Проверочных вопроса

### Вопрос 1 (легкий)
**Какой самый первый шаг при ошибке HTTP 400? Почему вы должны сделать его до того, как полезете в код?**

<details>
<summary>Ответ</summary>

**Самый первый шаг:** Посмотреть **тело ответа сервера**.

**Почему:** Сервер часто пишет ТОЧНУЮ причину ошибки в теле ответа!

**Пример из вашего лога:**
```json
{
  "ERRORS": {
    "captcha": ["Цифры с картинки введены неверно"],
    "captchaToken": ["Необходимо обновить картинку с цифрами"]
  }
}
```

**Это сразу говорит:**
1. Проблема с капчей (не с прокси, не с сетью)
2. Неправильно введены цифры
3. Токен устарел

**Без этого вы могли бы часы проверять прокси, SSL, DNS — но проблема была в другом.**

**Правило:** Сначала читаем ответ сервера. Потом — всё остальное.
</details>

### Вопрос 2 (средний)
**Вы получили ошибку, но в коде нет подробного логирования. Какие 3 команды вы выполните в терминале, чтобы вручную воспроизвести запрос и понять проблему?**

<details>
<summary>Ответ</summary>

**Команда 1: Базовый curl с verbose**
```bash
curl -v -X POST "https://service.nalog.ru/bi2-proc.json" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "Cookie: JSESSIONID=644ACE0802A2C16D4E4C72BF11FA88E1" \
  --data-urlencode "requestType=FINDPRS" \
  --data-urlencode "innPRS=2239000934" \
  --data-urlencode "bikPRS=044525225"
```

**Команда 2: Сохранить полный ответ в файл**
```bash
curl -v -X POST "https://..." \
  --output response.txt \
  --dump-header headers.txt \
  --trace-ascii trace.txt
```

**Команда 3: Использовать прокси (как в вашем боте)**
```bash
curl -v -x "193.3.23.126:51531" \
  --proxy-user "u3jKemhyaxtt:de2005c" \
  -X POST "https://service.nalog.ru/bi2-proc.json" \
  --data-urlencode "requestType=FINDPRS" \
  --data-urlencode "innPRS=2239000934"
```

**Что вы увидите:** Весь процесс подключения, отправки, получения ответа. Без необходимости лезть в код.
</details>

### Вопрос 3 (сложный)
**Представьте, что через месяц ваш бот снова упадет с ошибкой, но вы забыли все детали. Какую ОДНУ вещь вы должны добавить в код СЕЙЧАС, чтобы через месяц отладка заняла 5 минут, а не 5 часов?**

<details>
<summary>Ответ</summary>

**Добавить ФУНКЦИЮ СОХРАНЕНИЯ ПОЛНОГО КОНТЕКСТА ПРИ ОШИБКЕ.**

```php
// Добавить в конец getPage(), перед return
if ($info['http_code'] != 200) {
    $debugData = [
        'timestamp' => date('Y-m-d H:i:s'),
        'url' => $url,
        'http_code' => $info['http_code'],
        'post_params' => $postParams,
        'request_headers' => $requestHeaders ?? null,
        'response_headers' => $headers,
        'response_body' => substr($body, 0, 2000), // первые 2000 символов
        'verbose_log' => $verboseLog,
        'proxy' => $hostProxy['ip'] . ':' . $hostProxy['port'] ?? null,
        'curl_error' => $errorMsg,
    ];
    
    $filename = '/tmp/debug_' . date('Ymd_His') . '_' . md5($url) . '.json';
    file_put_contents($filename, json_encode($debugData, JSON_PRETTY_PRINT));
    
    // Также отправить в центральный лог
    error_log("[DEBUG] Saved to: $filename");
}
```

**Почему это спасет вас через месяц:**
- Вы увидите ТОЧНО те же параметры, что были при ошибке
- Не нужно воспроизводить проблему (это сложно)
- Есть полный verbose-лог
- Есть ответ сервера (с сообщением об ошибке)

**Через месяц вы просто:**
```bash
cat /tmp/debug_*.json | grep -A5 "ERRORS"
# И сразу видите причину!
```
</details>

---

## Рекомендуемая литература

| Тип | Название | Что дает |
|-----|----------|----------|
| **Книга** | "Debugging: The 9 Indispensable Rules for Finding Even the Most Elusive Software and Hardware Problems" (David Agans) | Ментальные модели отладки |
| **Статья** | "Rubber Duck Debugging" (The Pragmatic Programmer) | Простой метод найти ошибку |
| **Инструмент** | `curl --trace`, `curl --trace-ascii` | Детальнейший разбор запросов |
| **Документация** | Chrome DevTools Network Tab | Как копировать запросы как cURL |
| **Видео** | "Mastering Debugging in PHP" (YouTube, Laracasts) | 1 час практических советов |
| **Практика** | Postman → Code → cURL | Генерация команд из GUI |

---

## Для какой квалификации полезно знание?

| Квалификация | Уровень | Почему важно |
|--------------|---------|--------------|
| **Любой разработчик** | Обязательный | Отладка — 50% рабочего времени |
| **DevOps инженер** | Эксперт | Быстрое восстановление сервисов |
| **Tech Lead** | Продвинутый | Учит команду отлаживать эффективно |
| **Support инженер** | Средний | Сбор данных для разработчиков |
| **QA инженер** | Продвинутый | Создание воспроизводимых баг-репортов |

### Индикаторы мастерства отладки:

| Навык | Junior | Middle | Senior |
|-------|--------|--------|--------|
| Читает ошибку в консоли | ✅ | ✅ | ✅ |
| Использует var_dump/print_r | ✅ | ✅ | ✅ |
| Применяет xdebug/step debugging | ❌ | ✅ | ✅ |
| Воспроизводит запрос через curl | ❌ | ✅ | ✅ |
| Создает минимальный воспроизводимый пример | ❌ | ⚠️ | ✅ |
| Автоматизирует сбор контекста ошибок | ❌ | ❌ | ✅ |

---

## Итоговый вывод

**Ваш путь отладки (как было):**
```
Ошибка → гадание → изменение кода → снова ошибка → снова гадание (часы/дни)
```

**Ваш путь отладки (как должно быть):**
```
Ошибка → смотрю лог ошибки (уже сохранен!) → читаю тело ответа → 
сравниваю с успешным запросом → исправляю → готово (5-15 минут)
```

**Что сделать прямо сейчас:**

1. **Добавить в код функцию сохранения контекста при ошибке** (см. вопрос 3)
2. **Создать алиасы для быстрого доступа к логам** (см. раздел 7)
3. **Научить команду пользоваться curl --trace**
4. **Держать под рукой чек-лист из 10 шагов**

**Запоминающаяся фраза:**  
> "Отладка без сохранения контекста — это как искать черную кошку в темной комнате, где кошки нет. Сохраняйте всё при ошибке, и кошка сама придет к вам с признанием."