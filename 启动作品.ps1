param([switch]$NoBrowser)
$ErrorActionPreference = 'Stop'
$siteRoot = [System.IO.Path]::GetFullPath($PSScriptRoot)
$server = $null
for ($port = 8848; $port -lt 8890; $port++) {
    try {
        $candidate = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $port)
        $candidate.Start()
        $server = $candidate
        break
    } catch { if ($candidate) { $candidate.Stop() } }
}
if (-not $server) { throw 'No available local preview port.' }
$url = "http://127.0.0.1:$port/"
Write-Host "Shanhai Bestiary: $url"
Write-Host 'Keep this window open. Press Ctrl+C to stop.'
if (-not $NoBrowser) { Start-Process $url }
$mimeTypes = @{ '.html'='text/html; charset=utf-8'; '.js'='text/javascript; charset=utf-8'; '.css'='text/css; charset=utf-8'; '.webp'='image/webp'; '.png'='image/png'; '.jpg'='image/jpeg'; '.woff2'='font/woff2'; '.json'='application/json; charset=utf-8'; '.md'='text/plain; charset=utf-8' }
try {
    while ($true) {
        $client = $server.AcceptTcpClient()
        $client.ReceiveTimeout = 4000
        $client.SendTimeout = 4000
        try {
            $stream = $client.GetStream()
            $reader = [System.IO.StreamReader]::new($stream, [System.Text.Encoding]::ASCII, $false, 1024, $true)
            $requestLine = $reader.ReadLine()
            if (-not $requestLine) { continue }
            while ($reader.ReadLine()) {}
            $parts = $requestLine.Split(' ')
            $method = $parts[0]
            $relative = [System.Uri]::UnescapeDataString(($parts[1] -split '\?')[0]).TrimStart('/')
            if (-not $relative) { $relative = 'index.html' }
            $target = [System.IO.Path]::GetFullPath((Join-Path $siteRoot $relative))
            $inside = $target.StartsWith($siteRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)
            if ($method -ne 'GET' -and $method -ne 'HEAD') {
                $status = '405 Method Not Allowed'; $body = [System.Text.Encoding]::UTF8.GetBytes('Method not allowed'); $mime = 'text/plain'
            } elseif (-not $inside -or -not [System.IO.File]::Exists($target)) {
                $status = '404 Not Found'; $body = [System.Text.Encoding]::UTF8.GetBytes('Not found'); $mime = 'text/plain'
            } else {
                $status = '200 OK'; $body = [System.IO.File]::ReadAllBytes($target)
                $mime = $mimeTypes[[System.IO.Path]::GetExtension($target).ToLowerInvariant()]
                if (-not $mime) { $mime = 'application/octet-stream' }
            }
            $header = "HTTP/1.1 $status`r`nContent-Type: $mime`r`nContent-Length: $($body.Length)`r`nConnection: close`r`nX-Content-Type-Options: nosniff`r`n`r`n"
            $bytes = [System.Text.Encoding]::ASCII.GetBytes($header)
            $stream.Write($bytes,0,$bytes.Length)
            if ($method -ne 'HEAD') { $stream.Write($body,0,$body.Length) }
            $stream.Flush()
        } catch { Write-Verbose $_.Exception.Message } finally { $client.Close() }
    }
} finally { $server.Stop() }
