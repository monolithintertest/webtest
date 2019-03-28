#!/usr/local/bin/perl


##############################################################################
#
#	FormMailerDX 
#	v 1.01 
#	(C)CGI-LAND
#	happy@honesto.net
#	http://happy.honesto.net/cgi/
#
#	・このスクリプトを使用したことによるいかなる損害についても作者はその責を
#	　負いません
#	・有償/無償、改造の有無に関わらず、このスクリプトの無断での再配布や
#　　　直接的営利利用（レンタル・代行設置など）は禁止します
#	・スクリプトの改造は自由ですが著作権表示を見えなくする行為は禁止します
#   ・スクリプトの設置等に関するメールでのお問い合わせはご遠慮ください。
#	・必ず上記URLの利用規程をご確認の上でご利用ください。
##############################################################################


#jcode.plのパス
require'./jcode.pl';


#mimew.plのパス
require'./mimew.pl';


#管理者パスワード
$admin = 'abc';


#送信前の確認画面
#0:表示しない
#1:表示する
$confirm_key = 1;


#入力必須項目
#作成したHTMLフォームのname属性を指定します
#添付ファイルも必須に指定可能
#「'」で囲って「,」で区切る
#@req = ('a3','a4');


#確認画面テンプレートファイル
$template2 = './temp2.txt';


#メール送信先
#間違えるとメールが届きません！
$mailto = 'monolith@mono-net.co.jp';

#記入されたメールアドレスにも
#同じメールを控えとして送信（ccで送信します）
#0:しない
#1:する
$copy_key = 0;


#メールの最大文字数(bytes)
#ここで指定した文字数を超えるメールは送信できなくなります。
#全角文字１文字＝2bytes
#半角文字1文字＝1byte
$max_length = 3000;


#最大ファイルサイズ(bytes)
#ファイルサイズの合計が、ここで指定した値を超えると送信できません
$max_file_size = 300000;


#sendmailのパス
$sendmail = '/usr/sbin/sendmail';


#このスクリプトのファイル名
$scriptname = 'form.cgi';


#メールテンプレートファイル
$template = './temp.txt';


#添付ファイル一時保存ディレクトリ
#最後の/は付けない
$file_dir = './tmp';


#bodyタグ
#エラー表示画面や管理者モードで有効
$body_tag = '<body bg="#ffffff" text="#000000">';


#送信完了後に表示するHTMLのURL（httpから記入）
$jumpto = "./end.html";


#送信完了後のHTMLへのジャンプ
#0:Locationヘッダで移動（通常はこちら）
#1:METAタグで移動（Locationヘッダでうまくいかない場合はこちら）
$jump_header = 0;


#入力項目をタブ区切りテキストファイル（TSVファイル）に記録
#0:しない
#1:する
#ファイルには入力された個人情報も記録されます。
#取り扱いには充分ご注意ください。
$tsv_key = 0;


#TSVファイル作成ディレクトリ
#機密性の高い情報や住所・電話番号等の重要な個人情報等が
#記録される可能性がある場合は、public_htmlの外など
#ブラウザから直接アクセスできない場所に作成するなどの
#セキュリティ対策を行うことをお勧めします。
$tsv_dir = './tsv';


#TSVファイルを
#0:日毎に作成(作成されるファイル名：yymmdd)
#1:月毎に作成(yymm)
$tsv_name = 0;


#TSVファイルに記入する項目
#フォームのname属性で指定
#ここで指定した順序で記録されます。
#@tsv_items = ('a3','a4');


#TSVファイルの拡張子
#「.」は付けない
$tsv_ext = "txt";



#初期設定ここまで

&get_form;

if($mode eq ''){
	if($confirm_key){
		&confirm;
	}else{
		&send;
	}
}elsif($mode eq 'admin'){&admin_top;}
elsif($mode eq 'edit_form'){&edit_form;}
elsif($mode eq 'edit'){&edit;}
elsif($mode eq 'confirm'){&confirm;}
elsif($mode eq 'send'){&send;}
exit;


#-------------------------------------
#----管理者モードトップ
#-------------------------------------
sub admin_top{
	&header;
	print<<"HTML";
<center>
<form action="$scriptname" method="POST">
管理者パスワード：<input type="password" name="pass" size="8">
<input type="submit" value="OK">
<input type="hidden" name="mode" value="edit_form">
</form>
</center>
HTML
	&footer;
}


#-------------------------------------
#----メール編集フォーム
#-------------------------------------
sub edit_form{
	if($in{pass} ne $admin){&error("管理者パスワードが正しくありません");}
	open(TEMPLATE,$template) || &error("テンプレートファイルを開けません");
	@allbody = <TEMPLATE>;
	close(TEMPLATE);
	
	$subject = shift @allbody;
	$body = join("",@allbody);
	
	$subject =~ s/\n//g;
	
	&header;
	print<<"HTML";
<center>
<form action="$scriptname" method="POST">
<input type="hidden" name="mode" value="edit">
<input type="hidden" name="pass" value="$in{pass}">
<table border="1" width="80%">
<tr>
<th colspan="2">メールの編集</th>
</tr>
<tr>
<td align="right">件名：</td>
<td><input type="text" name="subject" size="40" value="$subject"></td>
</tr>
<tr>
<td align="right" valign="top">本文：</td>
<td>送信されるメールの本文を記述してください。<br>
・フォームに記入された項目を本文中に挿入するには&lt;#name属性#&gt;と記述します。<br>
　例）フォームに&lt;input type="text" name="住所" size="20"&gt;<br>
　という項目があり、ここに入力された値を本文中に表\示したい場合<br>
　&lt;#住所#&gt;と記入します。<br>
・送信者のホスト・IPを表\示したい場合はそれぞれ&lt;#host#&gt;、&lt#ip#&gtとしてください。<br>
<br>
<textarea cols="80" rows="20" name="body">$body</textarea></td>
</tr>
<tr>
<td colspan="2" align="center"><input type="submit" value="OK"></td>
</tr>
</table>
</form>
</center>
HTML

	&footer;
}


#-------------------------------------
#----メール編集
#-------------------------------------
sub edit{
	if($in{pass} ne $admin){&error("管理者パスワードが正しくありません");}
	
	if($in{subject} eq ''){&error("件名が記入されていません");}
	if($in{body} eq ''){&error("本文が記入されていません");}
	
	$in{subject} =~ s/\r\n//g;
	$in{subject} =~ s/\r//g;
	$in{subject} =~ s/\n//g;
	$in{subject} = &repair_tag($in{subject});
	
	$in{body} =~ s/\r\n/\n/g;
	$in{body} =~ s/\r/\n/g;
	$in{body} = &repair_tag($in{body});
	
	open(TEMPLATE,">$template") || &error("テンプレートファイルに書き込めません");
	print TEMPLATE $in{subject}."\n";
	print TEMPLATE $in{body};
	close(TEMPLATE);
	
	&header;
	print"<center>\n";
	print"更新しました<br>";
	print"<a href=\"$scriptname?mode=admin\">戻る</a>\n";
	print"</center>\n";
	&footer;
}


#-------------------------------------
#----送信
#-------------------------------------
sub send{

	if($confirm_key){#確認画面ありの場合の添付ファイル処理
		foreach $file (grep(/^file\d+$/,(keys %in))){
			$FILE_PATH{$file} = $in{"path_$file"};
			$FILE_NAME{$file} = $in{"name_$file"};
			binmode(FILE);
			open(FILE,$FILE_PATH{$file}) || &error("ファイルを開けません");
			while(<FILE>){
				$FILE_DATA{$file} .= $_;
			}
			close(FILE);
		}
	}
	
	&chk_req;#必須項目チェック	
	
	&send_mail;#メール送信
	
	if($tsv_key){&add_to_tsv;}#tsvファイルに加える
	
	&delete_old_file;
	
	&jump;#送信完了画面へ
}


#-------------------------------------
#----メール送信
#-------------------------------------
sub send_mail{
	open(TEMPLATE,$template) || &error("テンプレートファイルを開けません");
	@allbody = <TEMPLATE>;
	close(TEMPLATE);
	
	my $boundary = "boundary";#区切り
	
	my $subject = shift(@allbody);
	my $body = join("",@allbody);
	
	foreach $key (keys %in){#テンプレートと入力項目から本文作成
		if($confirm_key){#確認画面のURLエスケープを復元
			$in{$key} =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		}
		$in{$key} =~ s/\r\n/\n/g;
		$in{$key} =~ s/\r/\n/g;

		$body =~ s/\Q<#$key#>\E/$in{$key}/g;
	}

	### 検索エンジンから来た場合、キーワードをメールにセット ################################
	$seq=$ENV{'HTTP_COOKIE'};
	@seqid = split(/; */,$seq);
	foreach $seqid(@seqid){
		($cname,$cvalue) = split(/=/,$seqid);
		$cvalue =~ s/%([0-9A-Fa-f][0-9A-Fa-f])/pack("C", hex($1))/eg;

		if($cname eq 'engine_name'){ $engine_name = (split('engine_name=',$seqid))[1]; }
		if($cname eq 'keyword'){ $keyword = $cvalue; }
	}
	if($engine_name ne "" || $keyword ne ""){
		$body .= "
検索エンジン＝$engine_name
キーワード＝$keyword
";
		&Cookie_Clear();
	}
	#### ここまで #########################################################################

	if($copy_key){#コピーを送信する場合はメールアドレスチェックへ
		&chk_mail($in{MAIL});
	}
	
	#ホスト・IP表示	
	my($host,$ip) = &get_host;
	$body =~ s/\<\#host\#\>/$host/g;
	$body =~ s/\<\#ip\#\>/$ip/g;
	
	#未入力項目のタグ削除
	$body =~ s/\<\#.*\#\>//g;
	
	#長さチェック
	if(length($body) > $max_length){&error("最大文字数を超えています");}
	
	
	#件名エンコード
	$subject = &mimeencode(jcode'jis($subject));
	$subject =~ s/\n//g;
	
	#本文エンコード
	$body = jcode'jis($body);

	undef(@allbody);
	
	my $file_flag = 0;
	my $file_size = 0;
	foreach $file (grep(/^file\d+$/,(keys %FILE_DATA))){#添付ファイルの有無判定
		if($FILE_DATA{$file}){
			$file_flag++;
			$file_size += length($FILE_DATA{$file});#ファイルサイズ合計加算
		}
	}
	
	if($file_size > $max_file_size){&error("ファイルサイズの合計が大きすぎます");}

	open(MAIL,"|$sendmail -t -i") || &error("SENDMAILを開けません");
	
	if($file_flag){#添付ファイル有り
		
		#ヘッダ
		print MAIL "MIME-Version: 1.0\n";
		print MAIL "Content-Type: Multipart/Mixed; boundary=\"$boundary\"\n";
		print MAIL "Content-Transfer-Encoding:Base64\n";
		#print MAIL 'X-Mailer: FormMailerDX (C)CGI-LAND' ."\n";#削除改変不可
		print MAIL "From: $in{MAIL}\n";
		print MAIL "To: $mailto\n";
		if($copy_key){
			print MAIL "Cc: $in{MAIL}\n";
		}
		print MAIL "Subject: $subject\n";
	
		
		#本文
		print MAIL "--$boundary\n";
		print MAIL "Content-Type: text/plain; charset=\"ISO-2022-JP\"\n";
		print MAIL "\n";
		print MAIL "$body\n";
	
	
		#添付ファイル
		foreach $file (grep(/^file\d+$/,(keys %FILE_DATA))){ 	
			if($FILE_DATA{$file}){
				#$path = &save_file($FILE_DATA{$file},$FILE_NAME{$file});
				
				#添付ファイルエンコード
				$FILE_DATA{$file} = &bodyencode($FILE_DATA{$file});
				$FILE_DATA{$file} .= &benflush;
				
				print MAIL "--$boundary\n";
				print MAIL "Content-Type: application/octet-stream; name=\"$FILE_NAME{$file}\"\n";
				print MAIL "Content-Transfer-Encoding: base64\n";
				print MAIL "Content-Disposition: attachment; filename=\"$FILE_NAME{$file}\"\n";
				print MAIL "\n";
				print MAIL "$FILE_DATA{$file}\n";
				print MAIL "\n";
	
			}
		}
	
	
		#マルチパート終了
		print MAIL "--$boundary--\n";
		
		#一時保存添付ファイル削除
		foreach $file (grep(/^file\d+$/,(keys %FILE_DATA))){#添付ファイルの有無判定
			if(-e $FILE_PATH{$file}){unlink $FILE_PATH{$file};}
		}
		
	}else{#添付ファイル無し
		
		#ヘッダ
		print MAIL "Mime-Version: 1.0\n";
		print MAIL "Content-Type: text/plain; charset=ISO-2022-JP\n";		
		print MAIL "Content-Transfer-Encoding: 7bit\n";
		#print MAIL 'X-Mailer: FormMailerDX (C)CGI-LAND' ."\n";#削除改変不可
		print MAIL "To: $mailto\n";	
		print MAIL "From: $in{MAIL}\n";
		if($copy_key){
			print MAIL "Cc: $in{MAIL}\n";
		}
		print MAIL "Subject: $subject\n";
		print MAIL "\n";
		
		#本文
		print MAIL $body."\n";
		
	}
	close MAIL;

}

sub Cookie_Clear{
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time - 1*24*60*60);
	$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Wednesday"; $y4="Thursday"; $y5="Friday"; $y6="Saturday";
	$m0="Jan"; $m1="Feb"; $m2="Mar"; $m3="Apr"; $m4="May"; $m5="Jun"; $m6="Jul"; $m7="Aug"; $m8="Sep"; $m9="Oct"; $m10="Nov"; $m11="Dec";
	@youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6);
	@monthg = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11);
	$date_gmt = sprintf("%s\, %02d\-%s\-%04d %02d:%02d:%02d GMT",@youbi[$wdayg],$mdayg,@monthg[$mong],$yearg +1900,$hourg,$ming,$secg);

	print "Set-Cookie: engine_name=''; expires=$date_gmt; PATH=/ \n";
	print "Set-Cookie: keyword=''; expires=$date_gmt; PATH=/ \n";
}

#-------------------------------------
#----TSVファイルに記録
#-------------------------------------
sub add_to_tsv{

	foreach $n (@tsv_items){
		push(@tsv,$in{$n}); 
	}
	my $line = join("\t",@tsv);#入力項目を連結
	$line =~ s/\r\n//g;
	$line =~ s/\r//g;
	$line =~ s/\n//g;
	
	my($y,$m,$d) = &get_date;
	
	if(!$tsv_name){#TSVファイル名設定
		$tsv = "$y$m$d.$tsv_ext";
	}else{
		$tsv = "$y$m.$tsv_ext";
	}
	
	if($confirm_key){#確認画面のURLエスケープを復元
		$line =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
	}
	$line =~ s/\r\n//g;
	$line =~ s/\r//g;
	$line =~ s/\n//g;
	open(TSV,">>$tsv_dir/$tsv") || &error("$tsv_dir/$tsv.$tsv_ext:TSVファイルに書き込めません");
	print TSV $line."\n";
	close(TSV);
	
}


#-------------------------------------
#----古い一時保存ファイルを削除
#-------------------------------------
sub delete_old_file{
	my $file;
	opendir(DIR,$file_dir);
	while($file = readdir(DIR)){
		if($file eq '.' || $file eq '..'){next;}
		if(time - (stat("$file_dir/$file"))[9] > 24*60*60){
			unlink("$file_dir/$file") || &error("$file_dir/$fileを削除できません");
		}
		
	}
	closedir(DIR);
}


#-------------------------------------
#----確認画面
#-------------------------------------
sub confirm{

	&chk_req;#必須項目チェック
	if($copy_key){#コピーを送信する場合はメールアドレスチェックへ
		&chk_mail($in{MAIL});
	}
	
	my @files;
	my $file_flag = 0;
	
	foreach $file (grep(/^file\d+$/,(keys %FILE_DATA))){
		if($FILE_DATA{$file} ne ''){
			$path = &save_file($FILE_DATA{$file},$FILE_NAME{$file});
			$FILE_PATH{$file} = $path;
			$file_flag++;
		}
	}
	
	print"Content-type: text/html\n\n";
	
	open(TEMP2,"$template2") || &error("確認画面テンプレートを開けません");
	$body = join("",<TEMP2>);
	close(TEMP2);
		
	#各項目
	foreach $key (keys %in){
		$escaped{$key} = $in{$key};
		
		$in{$key} = &del_tag($in{$key});#タグ除去
		$in{$key} =~ s/\r\n/<br>/g;
		$in{$key} =~ s/\r/<br>/g;
		$in{$key} =~ s/\n/<br>/g;
		
		$escaped{$key} =~ s/(\W)/'%'.unpack('H2',$1)/eg;#URLエスケープ		
		$hidden = "<input type=\"hidden\" name=\"$key\" value=\"$escaped{$key}\">";
		$body =~ s/\Q<#$key#>\E/$in{$key}$hidden/g;
	}
	
	#添付ファイル
	foreach $file (grep(/^file\d+$/,(keys %FILE_DATA))){
		if($FILE_DATA{$file} eq ''){next;}
		$file_hidden .= "<a href=\"$FILE_PATH{$file}\">$FILE_NAME{$file}</a> ";
		$file_hidden .= "<input type=\"hidden\" name=\"$file\" value=\"$FILE_NAME{$file}\">";
		$file_hidden .= "<input type=\"hidden\" name=\"path_$file\" value=\"$FILE_PATH{$file}\">";
		$file_hidden .= "<input type=\"hidden\" name=\"name_$file\" value=\"$FILE_NAME{$file}\">";
	}
	$body =~ s/\<\#file\#\>/$file_hidden/g;
	
	$body =~ s/\<\#.*\#\>//g;#未入力項目のタグ削除
	

	$body =~ s/\<\/body\>//g;
	$body =~ s/\<\/html\>//g;
	print $body;
	&footer;


}


#-------------------------------------
#----フォーム入力取得
#-------------------------------------
sub get_form{
	if($ENV{'REQUEST_METHOD'} eq "POST"){
	    if($ENV{'CONTENT_TYPE'} =~ m|multipart/form-data; boundary=([^\r\n]*)$|io){
			&decode_form_multipart($1);
		}else{
			read(STDIN,$buffer,$ENV{'CONTENT_LENGTH'});
			&decode_form;
		}
	}else { 
		$buffer = $ENV{'QUERY_STRING'}; 
		&decode_form;
	}
	$mode = $in{'mode'};
}


#-------------------------------------
#----フォーム入力デコード
#-------------------------------------
sub decode_form{
	@pairs = split(/&/,$buffer);
	foreach $pair (@pairs) {
		($name,$value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C",hex($1))/eg;
		&jcode'convert(*value,'sjis');
		
		#$value = &del_tag($value);
		
		#同じname属性の場合
		if($in{$name} ne ''){
			$in{$name} .= " ".$value;
		}else{
			$in{$name} = $value;
		}
	}
}


#-------------------------------------
#----マルチパートフォームデコード
#-------------------------------------
sub decode_form_multipart{
	my($bound) = @_;
 	my($que,$remain,$tmp,@arr);
	$CRLF = "\r\n";
	$que = "$CRLF";
	$remain = $ENV{'CONTENT_LENGTH'};

	binmode(STDIN);
	while($remain){
		$remain -= sysread(STDIN,$tmp,$remain) || &error($!);
		$que .= $tmp;
	}

	@arr = split(/$CRLF-*$bound-*$CRLF/,$que);
	shift(@arr);
	foreach(@arr){
		$tmp = $_;

		if(/^Content-Disposition: [^;]*; name="[^;]*"; filename="[^;]*"/io){
			$tmp =~ s/^Content-Disposition: ([^;]*); name="([^;]*)"; filename="([^;]*)"($CRLF)Content-Type: ([^;]*)$CRLF$CRLF//io;
			$FILE_DATA{$2} = $tmp;
			$FILE_NAME{$2} = $3;
			$FILE_TYPE{$2} = $4;

		}elsif(/^Content-Disposition: [^;]*; name="[^;]*"/io){
			$tmp =~ s/^Content-Disposition: [^;]*; name="([^;]*)"$CRLF$CRLF//io;
			&jcode::convert(\$tmp,'sjis');
			&jcode::convert(\$1,'sjis');

			#$tmp = &del_tag($tmp);
			
			#同じname属性の場合
			if($in{$1} ne ''){
				$in{$1} .= " ".$tmp;
			}else{
				$in{$1} = $tmp;
			}
		}
	}
	
	foreach $k (keys %FILE_NAME){
		my @path = split(/\\/,$FILE_NAME{$k});
		$FILE_NAME{$k} = @path[$#path];
	}
}


#-------------------------------------
#----ファイル保存
#-------------------------------------
sub save_file{
	my($file_data,$file_name) = @_;

	open(IMG,">$file_dir/$file_name") || &error("ファイルを保存できません");
	print IMG $file_data;
	close(IMG);
	chmod 0666,"$file_dir/$file_name";

	return "$file_dir/$file_name";
}


#-------------------------------------
#----送信完了後移動
#-------------------------------------
sub jump{
	if(!$jump_header){#Location
		print"Location:$jumpto\n\n";
	}else{#META
		print"Content-type :text/html\n\n";
		print"<html>\n";
		print"<head>\n";
		print"<meta http-equiv=\"Refresh\" content=\"0;URL=$jumpto\">\n";
		print"</head>\n";
		print"<body bgcolor=\"#ffffff\">\n";
		print"更新中・・・<Br>";
		print"しばらく待っても移動しない場合は<br>\n";
		print"<a href=\"$jumpto\">こちら</a>をクリックしてください\n";
		print"</body>\n";
		print"</html>\n";
	}
}


#-------------------------------------
#----必須項目チェック
#-------------------------------------
sub chk_req{
	foreach $req (@req){
		if($req =~ /^file\d+$/ && $FILE_DATA{$req} eq ''){#ファイルの場合
			&error("$reqが指定されていません");
		}
		if($req !~ /^file\d+$/ && $in{$req} eq ''){#ファイル以外の項目
			&error("$reqが入力されていません");
		}
	}
}


#-------------------------------------
#----ヘッダ出力
#-------------------------------------
sub header{
	print"Content-Type:text/html\n\n";
	print<<"eof";
<html>
<head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<STYLE type="text/css">
<!--
body,tr,td,th,blockquote{font-size:$font_size}
-->
</STYLE>
<title>$title</title>
</head>
$body_tag
<br>
eof
}


#-------------------------------------
#----フッタ著作権表示（削除・変更不可）
#-------------------------------------
sub footer{
	#print"<hr>\n";
	#print"<div align=\"right\"><small><a href=\"http://happy.honesto.net/cgi/\">FORMMAILER DX&nbsp;CGI-LAND</a></small></div>\n";
	print"</body>\n";
	print"</html>\n";
}


#-------------------------------------
#----メールアドレスチェック
#-------------------------------------
sub chk_mail{
	my $chk = $_[0];
	if($chk eq ''){&error("メールアドレスが記入されていません");}
	if($chk =~ /\,/){ &error("メールアドレスにコンマ（,）が含まれています"); }
	if($chk !~ /[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,3}/){
		&error("メールアドレスが全角で記入されているか、書式が正しくありません");
	}
}


#-------------------------------------
#---日時取得
#-------------------------------------
sub get_date{
	my($sec,$min,$hour,$mday,$mon,$year,$wdy,$yday,$isdst) = localtime(time);
	$mon++;
	$year += 1900;
	$year = substr($year,-2,2);
	if($mon < 10){$mon = "0$mon";}
	if($mday < 10){$mday = "0$mday";}
	if($hour < 10){$hour = "0$hour";}
	if($min < 10){$min = "0$min";}
	if($sec < 10){$sec = "0$sec";}
	$youbi = ('(Sun)','(Mon)','(Tue)','(Wed)','(Thu)','(Fri)','(Sat)')[$wdy];
	return($year,$mon,$mday,$hour,$min,$sec,$youbi);
}


#-------------------------------------
#----ホスト・IP取得
#-------------------------------------
sub get_host{
	my ($ip,$host);
	$ip = $ENV{'REMOTE_ADDR'};
	$host = $ENV{'REMOTE_HOST'};
	if($host eq '' || $host eq $ip){$host = gethostbyaddr(pack("C4",split(/\./,$ip)),2);}
	if($host eq ''){$host = $ip;}
	return($host,$ip);
}


#-------------------------------------
#----タグ除去
#-------------------------------------
sub del_tag{
	my $str = $_[0];
	$str =~ s/&/&amp;/g;
	$str =~ s/,/&#44;/g;
	$str =~ s/</&lt;/g;
	$str =~ s/>/&gt;/g;
	$str =~ s/\"/&quot;/g;
	return $str;
}


#-------------------------------------
#----タグ修復
#-------------------------------------
sub repair_tag{
	my $str = $_[0];
	$str =~ s/&lt;/</g;
	$str =~ s/&gt;/>/g;
	$str =~ s/&quot;/"/g;#"
	return $str;
}


#-------------------------------------
#----エラー表示
#-------------------------------------
sub error{
	if($_[1]){&unlock;}
	&header;
	print "<br>$_[0]";
	print"<br>ブラウザの[Back(戻る)]ボタンで戻ってください";
	&footer;
	exit;
}

