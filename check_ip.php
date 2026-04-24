<?php
/**
 * Debug script to check MW environment
 */
require_once __DIR__ . '/autoload.php';
require_once __DIR__ . '/includes/Defines.php';
require_once __DIR__ . '/includes/Setup.php';

global $IP, $wgExtensionDirectory, $wgAutoloadLocalClasses;

echo "IP: $IP\n";
echo "ExtensionDirectory: $wgExtensionDirectory\n";
echo "Cite extension.json exists: " . (file_exists("$IP/extensions/Cite/extension.json") ? "YES" : "NO") . "\n";
echo "ExtensionRegistry class exists: " . (class_exists("ExtensionRegistry") ? "YES" : "NO") . "\n";
echo "wfLoadExtension function exists: " . (function_exists("wfLoadExtension") ? "YES" : "NO") . "\n";

// Try loading Cite manually
if (function_exists("wfLoadExtension")) {
    echo "\nTrying wfLoadExtension('Cite')...\n";
    wfLoadExtension('Cite');
    echo "After loading, ExtensionRegistry queue:\n";
    $qi = ExtensionRegistry::getInstance()->getQueue();
    echo "  Queued: " . implode(", ", array_keys($qi)) . "\n";
}
