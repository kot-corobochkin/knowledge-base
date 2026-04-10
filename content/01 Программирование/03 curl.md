curl -v https://api.telegram.org
* Rebuilt URL to: https://api.telegram.org/
*   Trying 149.154.166.110... 
[ДНС работает]
* TCP_NODELAY set
* Connected to api.telegram.org (149.154.166.110) port 443 (#0)
[TCP установился]
* ALPN, offering h2
* ALPN, offering http/1.1
[ALPN — это: Application-Layer Protocol Negotiation
Механизм внутри TLS, который говорит:
> "Какой протокол будем использовать после установки защищённого соединения?"]

* successfully set certificate verify locations:
*   CAfile: /etc/pki/tls/certs/ca-bundle.crt
  CApath: none
[**curl нашёл сертификаты доверенных центров (CA)** и готов проверять SSL-сертификат сервера.]
* TLSv1.3 (OUT), TLS handshake, Client hello (1):

curl -v -x http://PPR149QWUXS:J8oFv32HyM8Mgz@193.233.217.3:3082 https://api.telegram.org

curl -v -x http://PPR149QWUXS:J8oFv32HyM8Mgz@193.233.217.3:3082 https://api.telegram.org

```

$apiUrl = "https://api.telegram.org/bot{$this->botToken}/sendMessage";

$proxy = "193.233.217.3:3082";
$proxyAuth = "PPR149QWUXS:J8oFv32HyM8Mgz";

$ch = curl_init();

curl_setopt_array($ch, [
    CURLOPT_URL => $apiUrl,
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => $queryData,
    CURLOPT_RETURNTRANSFER => true,

    // прокси
    CURLOPT_PROXY => $proxy,
    CURLOPT_PROXYUSERPWD => $proxyAuth,
    CURLOPT_PROXYTYPE => CURLPROXY_HTTP,

    // полезно для отладки
    CURLOPT_TIMEOUT => 30,
]);

$result = curl_exec($ch);

if ($result === false) {
    echo "Curl error: " . curl_error($ch);
} else {
    $response = json_decode($result, true);
    var_dump($response);
}

curl_close($ch);

```