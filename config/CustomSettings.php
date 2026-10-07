<?php
$wgSitename = 'Time Appliances Project';
$wgMetaNamespace = 'TAP';
$wgServer = rtrim(getenv('MW_SERVER') ?: 'http://localhost:8088', '/');
$wgCanonicalServer = $wgServer;
$wgScriptPath = '';
$wgDefaultSkin = 'vector';
$wgVectorDefaultSkinVersion = '1';
$wgVectorDefaultSkinVersionForExistingAccounts = '1';
$wgVectorDefaultSkinVersionForNewAccounts = '1';
$wgLogo = "$wgScriptPath/images/tap-logo.png";
$wgLogos = [ '1x' => $wgLogo, 'icon' => $wgLogo ];
$wgHooks['BeforePageDisplay'][] = static function ( $out, $skin ) {
    $out->addInlineStyle('.mw-wiki-logo { background-size: 135px auto; }');
};
$wgEnableEmail = false;
$wgEnableUserEmail = false;
$wgEnableUploads = true;
$wgFileExtensions = [ 'png', 'gif', 'jpg', 'jpeg', 'webp', 'pdf', 'svg' ];
$wgGroupPermissions['*']['edit'] = false;
$wgGroupPermissions['*']['createaccount'] = false;
$wgGroupPermissions['user']['edit'] = true;
$wgGroupPermissions['sysop']['createaccount'] = true;
$wgGroupPermissions['sysop']['editinterface'] = true;
$wgCookieSecure = str_starts_with($wgServer, 'https://');
$wgRightsPage = 'TAP:Copyrights';
$wgRightsUrl = 'https://creativecommons.org/licenses/by/4.0/';
$wgRightsText = 'Creative Commons Attribution 4.0 International';
$wgRightsIcon = '';
$wgCacheDirectory = '/tmp/mediawiki-cache';
// Source editing, section editing, revision history, and discussion are built in.
// Use the bundled visual editor as an additional editing option.
wfLoadExtension('VisualEditor');
$wgDefaultUserOptions['visualeditor-enable'] = 1;
$wgVisualEditorAvailableNamespaces = [ NS_MAIN => true, NS_PROJECT => true ];
