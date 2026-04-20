## Теория: Smarty5 Module для Laminas (Delta System)

Отличный код! Это **кастомная реализация интеграции Smarty 5 с Laminas MVC**. Разберем его полностью, как если бы вы учились с нуля.

---

## 1. Общая архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                    Laminas MVC Application                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Delta\System\Smarty5 Module                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ module.config.php (главный конфиг модуля)            │    │
│  └─────────────────────────────────────────────────────┘    │
│                              │                               │
│                              ▼                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Renderer     │  │ Strategy     │  │ Resolver     │      │
│  │ (основной    │  │ (стратегия   │  │ (поиск       │      │
│  │ класс)       │  │ рендеринга)  │  │ шаблонов)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Smarty 5 Engine                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Разбор module.config.php

### Секция 'smarty' — настройки Smarty

```php
'smarty' => [
    'suffix' => 'tpl',           // Расширение файлов шаблонов
    'compile_dir' => getcwd() . '/data/smarty/templates_c',  // Скомпилированные шаблоны
    'cache_dir' => getcwd() . '/data/smarty/cache/templates', // Кэш HTML
    'plugins_dir' => getcwd() . '/data/smarty/plugins',      // Пользовательские плагины
    'options' => [],              // Доп. опции Smarty
    'escape_html' => false,       // Автоматическое экранирование HTML
    'caching' => false,           // Кэширование HTML (выключено)
    'force_standalone' => false,  // Режим работы (не изолирован)
]
```

**Важные моменты:**
- `getcwd()` — возвращает **корневую директорию проекта** (там, где запущен index.php)
- Все пути **абсолютные**, что хорошо для консольных команд и cron

### Секция 'service_manager' — регистрация сервисов

```php
'service_manager' => [
    'aliases' => [           // Псевдонимы для удобного доступа
        'SmartyStrategy' => Strategy::class,
        'SmartyRenderer' => Renderer::class,
    ],
    'factories' => [         // Фабрики для создания объектов
        'SmartyResolver' => ResolverFactory::class,
        Strategy::class => StrategyFactory::class,
        Renderer::class => RendererFactory::class,
    ],
]
```

**Как это работает:**
```php
// Где-то в коде можно получить сервис:
$renderer = $container->get('SmartyRenderer');  // через алиас
$renderer = $container->get(Renderer::class);   // через класс
```

### Секция 'controller_plugins' — плагины для контроллеров

```php
'controller_plugins' => [
    'aliases' => [
        'renderer' => RendererPlugin::class,  // В контроллере: $this->renderer()
    ],
]
```

### Секция 'view_manager' — подключение к Laminas

```php
'view_manager' => [
    'strategies' => [
        'SmartyStrategy',  // Говорит Laminas: "Используй Smarty для отображения"
    ],
]
```

**Важно:** Здесь **нет** `enable_cache`! Значит, кэширование на уровне Laminas **отключено по умолчанию**.

---

## 3. Разбор RendererFactory (фабрика рендерера)

Этот файл **создает основной объект Smarty** и настраивает его.

### Пошаговый разбор:

```php
public function __invoke(ContainerInterface $container, $requestedName, ?array $options = null): Renderer
{
    // 1. Получаем конфигурацию приложения
    $config = $container->get('configuration');
    $config = $config['smarty'];  // Берем только настройки Smarty

    // 2. Получаем другие сервисы
    $pathResolver = $container->get('SmartyTemplatePathStack');  // Где искать шаблоны
    $resolver = $container->get('SmartyResolver');               // Разрешение имен шаблонов
    $view = $container->get(View::class);                        // Laminas View

    // 3. Создаем и настраиваем объект Smarty
    $smarty = new Smarty();
    $smarty->setCompileDir($config['compile_dir']);     // Папка для скомпилированных
    $smarty->setEscapeHtml($config['escape_html']);     // Экранирование HTML
    $smarty->setTemplateDir($pathResolver->getPaths()->toArray()); // Где лежат .tpl
    $smarty->setCaching($config['caching']);            // Включить/выключить кэш
    $smarty->setCacheDir($config['cache_dir']);         // Папка для кэша
    $smarty->setForceCompile($config['force_compile']); // Принудительная компиляция
    $smarty->addPluginsDir($config['plugins_dir']);     // Плагины

    // 4. Создаем рендерер (обертку над Smarty для Laminas)
    $renderer = new Renderer($view, $smarty, $resolver);
    $renderer->setHelperPluginManager($container->get('ViewHelperManager'));
    
    // 5. Режим "standalone"
    if (isset($config['force_standalone']) && $config['force_standalone']) {
        $renderer = $renderer->setForceStandalone(true);
    }
    
    // 6. Настройка basePath хелпера
    $plugin = $renderer->plugin('basePath');
    $plugin->setBasePath('/');
    
    return $renderer;
}
```

### Ключевые методы Smarty:

| Метод | Что делает |
|-------|-----------|
| `setCompileDir()` | Куда сохранять скомпилированные PHP-версии шаблонов |
| `setCacheDir()` | Куда сохранять кэш HTML |
| `setCaching()` | Включить/выключить кэширование (0/1/2) |
| `setForceCompile()` | Перекомпилировать при каждом запросе (для разработки) |
| `setEscapeHtml()` | Автоматически экранировать вывод (безопасность) |
| `addPluginsDir()` | Где искать кастомные плагины Smarty |

---

## 4. Где физически лежат файлы (из этого кода)

```
Проект/
├── data/
│   └── smarty/
│       ├── templates_c/      ← Скомпилированные шаблоны (PHP)
│       ├── cache/
│       │   └── templates/    ← Кэш HTML (если включен)
│       └── plugins/          ← Пользовательские плагины
├── module/
│   └── Delta/
│       └── System/
│           └── Smarty5/      ← Код модуля
└── public/
    └── index.php             ← getcwd() указывает сюда
```

---

## 5. Почему у вас всё равно кэшировалось? (ответ из кода)

В **этом конфиге**:
- `'caching' => false` — HTML-кэш Smarty выключен
- `'force_compile'` — **НЕ ЗАДАН** в массиве `options` (используется значение по умолчанию Smarty = false)

### Где мог быть кэш:

1. **В `force_compile = false`** (по умолчанию) — Smarty НЕ перекомпилирует шаблоны при каждом запросе
2. **OPcache кэшировал** скомпилированные PHP-файлы из `data/smarty/templates_c/`
3. **Браузер кэшировал** HTTP-ответ

---

## 6. Как отключить ВСЁ кэширование в этой архитектуре

```php
// config/autoload/smarty.global.php (переопределяем настройки модуля)
'smarty' => [
    'caching' => false,           // Уже выключено
    'force_compile' => true,      // ← ДОБАВИТЬ! Принудительная компиляция
    'options' => [
        'force_compile' => true,  // Или здесь
    ],
]

// ИЛИ напрямую в фабрике (но лучше в конфиге)
```

**После добавления `force_compile = true`:**
- Smarty будет перекомпилировать шаблоны при КАЖДОМ запросе
- Старые скомпилированные файлы не используются
- OPcache не мешает (файлы всё равно новые)

**Минус:** снижение производительности. Только для разработки!

---

## 3 Проверочных вопроса

### Вопрос 1 (базовый)
**Почему в коде используется `getcwd() . '/data/smarty/...'`, а не относительные пути типа `'./data/smarty'`?**

<details>
<summary>Ответ</summary>

`getcwd()` возвращает **абсолютный путь** к корню проекта. Это гарантирует, что Smarty найдет папки независимо от того:
- Из какой директории запущен PHP-скрипт
- Запущен ли скрипт через CLI (cron, консольные команды)
- Используются ли символические ссылки

Относительные пути могут сломаться при вызове из другого места (например, из `bin/console`).
</details>

---

### Вопрос 2 (ситуационный)
**Вы добавили новый плагин Smarty в папку `data/smarty/plugins`, но он не работает. Что нужно проверить в коде фабрики?**

<details>
<summary>Ответ</summary>

Проверить, что:
1. **Путь добавлен через `addPluginsDir()`** — в коде это есть: `$smarty->addPluginsDir($config['plugins_dir'])`
2. **В конфиге указан правильный путь** — `'plugins_dir' => getcwd() . '/data/smarty/plugins'`
3. **Плагин назван по правилам Smarty** — например, `modifier.foo.php` для модификатора `foo`
4. **Права на чтение** папки и файла

**Проверка в коде:**
```php
$dirs = $smarty->getPluginsDir(); // Получить все папки с плагинами
var_dump($dirs);
```
</details>

---

### Вопрос 3 (продвинутый)
**В чем разница между `setCaching(false)` и `setForceCompile(true)`? Когда использовать каждый?**

<details>
<summary>Ответ</summary>

| Параметр | Что делает | Когда использовать |
|----------|-----------|-------------------|
| `setCaching(false)` | Smarty НЕ сохраняет готовый HTML | Постоянно на проде (если не нужен кэш) |
| `setForceCompile(true)` | Перекомпилировать шаблон при КАЖДОМ запросе | **Только на разработке** при частом изменении .tpl |

**Важно:** 
- `caching = false` — не отключает компиляцию, просто не сохраняет HTML
- `force_compile = true` — заставляет перекомпилировать даже если PHP-версия уже есть

**Пример комбинации для разработки:**
```php
'caching' => false,        // Не сохраняем HTML
'force_compile' => true,   // Всегда пересобираем шаблоны
```

**Пример для продакшена:**
```php
'caching' => true,         // Включить кэш для скорости
'force_compile' => false,  // Не тратить ресурсы на перекомпиляцию
```
</details>

---

## Литература

1. **Smarty 5 Official Docs** — smarty.net/docs/
2. **Laminas View Layer** — docs.laminas.dev/laminas-view/
3. **Laminas Service Manager** — docs.laminas.dev/laminas-servicemanager/
4. **Laminas Controller Plugins** — docs.laminas.dev/laminas-mvc/plugins/
5. **getcwd() vs __DIR__** — www.php.net/manual/ru/function.getcwd.php

---

## Для какой квалификации полезно знание этого кода?

| Квалификация | Полезность | Что дает понимание |
|--------------|------------|-------------------|
| **Junior** | ⭐⭐ | Понимание, как подключаются шаблонизаторы |
| **Middle** | ⭐⭐⭐⭐⭐ | Умение настраивать Smarty в Laminas, находить пути кэша, отлаживать проблемы |
| **Senior** | ⭐⭐⭐⭐ | Архитектура интеграции, создание кастомных модулей, фабрик, сервисов |
| **DevOps** | ⭐⭐ | Понимание, куда приложение пишет файлы, для настройки бэкапов и очистки |

### Ключевые навыки, которые вы развиваете:

1. **Service Manager (DI-контейнер)** — понимание фабрик и алиасов
2. **View Layer архитектура** — как Laminas работает с шаблонами
3. **Smarty конфигурация** — все параметры и их влияние
4. **Файловая система в PHP** — абсолютные vs относительные пути
5. **Отладка кэша** — многоуровневое кэширование (Laminas → Smarty → OPcache)

---

## Итог: почему страница кэшировалась?

```php
// В вашем конфиге было:
'smarty' => [
    'caching' => false,        // ✅ HTML-кэш выключен
    'force_compile' => ???,    // ❌ НЕ БЫЛО ЗАДАНО (по умолчанию false)
]

// Что происходило:
1. Smarty скомпилировал шаблон в PHP (один раз)
2. Скомпилированный PHP сохранился в data/smarty/templates_c/
3. При следующих запросах использовался он (экономия времени)
4. OPcache закэшировал этот PHP в памяти сервера
5. Вы меняли .tpl, но Smarty не перекомпилировал (force_compile = false)

// Решение: добавить на время разработки
'force_compile' => true,
```

Теперь вы полностью понимаете, как работает этот модуль! 🎯