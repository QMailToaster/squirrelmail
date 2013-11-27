<?php
####################
# Local configuration for Qmail Toaster
# configure to suit your requirements

# these were in the former toaster config,
#     changed/removed for stock dovecot (w/out courier compat config)
# $imap_server_type = 'courier';
# $optional_delimiter = '.';
# $default_folder_prefix = 'INBOX.';
# $delete_folder = true;
# $show_contain_subfolders_option = false;

$org_name        = "QmailToaster";
# $org_logo        = SM_PATH . 'images/sm_logo.png';
# $org_logo_width  = '308';
# $org_logo_height = '111';
# $org_title       = "SquirrelMail $version";
$provider_uri    = 'http://qmailtoaster.com/';
$provider_name   = 'QmailToaster';

# smtp server options
$smtpServerAddress  = 'localhost';
$smtpPort           = 587;
$smtp_auth_mech     = 'login';

# imap server options
$imapServerAddress  = 'localhost';
$imap_server_type   = 'dovecot';
# SM doesn't support starttls until v1.5.1, so we'll use digest-md5 til then
#$use_imap_tls       = true;
$imap_auth_mech     = 'digest-md5';

$useSendmail              = false;
$optional_delimiter       = 'detect';
$default_folder_prefix    = '';
$show_prefix_option       = false;
$force_username_lowercase = true;
$hide_sm_attributions     = true;

$plugins[] = 'calendar';
$plugins[] = 'notes';
$plugins[] = 'filters';
$plugins[] = 'quota_usage';
$plugins[] = 'unsafe_image_rules';
$plugins[] = 'qmailadmin_login';

?>
