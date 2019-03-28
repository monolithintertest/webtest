#!/usr/local/bin/perl5

use Jcode;

$ENGINE_FILENAME = "/home/users/0/lolipop.jp-dp46057159/web/monolith-link.com/contact/engine.dat";

$str = $ENV{'QUERY_STRING'};
@part = split('&&', $str);
foreach $i (@part) {
	($variable,$value) = split('=x=',$i);
	if($variable eq 'ref'){ $keepurl = $value; }
	$value =~ tr/+/ /;
	$value =~ s/%([0-9a-fA-F][0-9a-fA-F])/pack("C", hex($1))/eg;
	$str_code = &Jcode::getcode(\$value);
	&Jcode::convert(\$value,"sjis","$str_code");
	$in{$variable} = $value;
}

$ref = $in{ref};

##### キーワードの登録(検索サイトから来た場合のみ)
open(ENGINE,"$ENGINE_FILENAME");
@enginedata = <ENGINE>;
close(ENGINE);

for($i=0,$ivalue="",$engine_name="";$i<@enginedata;$i++){
	$engineurl = (split('{}',@enginedata[$i]))[1];
	$l_engineurl = $engineurl;
	$l_engineurl =~ tr/a-z/A-Z/;
	if(($ref =~ /$engineurl/) || ($ref =~ /$l_engineurl/)){
		($engine_name,$engineurl,$keyword,$etc) = split('{}',@enginedata[$i]);
		$keyword =~ s/\r\n|\r|\n//g;
		$arg_str = (split('\?',$ref))[1];
		@refdata = split('&',$arg_str);
		for($m=0;$m<@refdata;$m++){
			if((split('=',@refdata[$m]))[0] eq $keyword){
				($iname,$ivalue) = split('=',@refdata[$m]);
				$ivalue =~ s/ |　/ /g;
				##### COOKIEに検索エンジン名と検索キーワードをセット
				&Cookie_Set($keepurl,$ivalue);
				last;
			}
		}
	}
}

&Output_Spacer_Image;
exit;

##### COOKIEにSEQUENCEKEYのセット ####################
sub Cookie_Set{
	my ($engine,$ival,$etc) = @_;
	($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg) = gmtime(time + 3*24*60*60);
	$y0="Sunday"; $y1="Monday"; $y2="Tuesday"; $y3="Wednesday"; $y4="Thursday"; $y5="Friday"; $y6="Saturday";
	$m0="Jan"; $m1="Feb"; $m2="Mar"; $m3="Apr"; $m4="May"; $m5="Jun"; $m6="Jul"; $m7="Aug"; $m8="Sep"; $m9="Oct"; $m10="Nov"; $m11="Dec";
	@youbi = ($y0,$y1,$y2,$y3,$y4,$y5,$y6);
	@monthg = ($m0,$m1,$m2,$m3,$m4,$m5,$m6,$m7,$m8,$m9,$m10,$m11);
	$date_gmt = sprintf("%s\, %02d\-%s\-%04d %02d:%02d:%02d GMT",@youbi[$wdayg],$mdayg,@monthg[$mong],$yearg +1900,$hourg,$ming,$secg);

	print "Set-Cookie: engine_name=$engine; expires=$date_gmt; domain=dream-bank.biz; path=/; \n";
	print "Set-Cookie: keyword=$ival; expires=$date_gmt; domain=dream-bank.biz; path=/; \n";
}

sub Output_Spacer_Image{
	##### スペース画像の表示(0x0)
	print "Content-type:image/gif\n\n";
	binmode(STDOUT);
	open(IN,'/spacer.gif');
	binmode(IN);
	while(<IN>){print;}
	close(IN);
	exit;
}
