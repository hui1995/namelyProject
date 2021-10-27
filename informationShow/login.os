var pubpack = new JavaPackage ( "com.xlsgrid.net.pub" );
var javapack = new JavaPackage ( "java.lang" );
var jsonpack = new JavaPackage ( "com.alibaba.fastjson" );
var itspack= new JavaPackage ( "com.xmidware.its");
var mspack= new JavaPackage ( "com.xmidware.ms.controller");
var pubjson = new JavaPackage ("net.sf.json" );
var regexpack = new JavaPackage ( "java.util.regex" );

//查询机构手机号
function QueryLocInfo(){
	var ret = formatJsonVer(1,"OK","{}");
	var db=DBConectSQL();
  	var id = pubpack.EAFunc.NVL( request.getAttribute("id"),"");
    var sql="select guid from loc where id='"+id+"'";
    var ds=db.QuerySQL(sql);
    if( ds.getRowCount()<=0 ) {
			ret=formatJsonVer(-1,"该账户不存在","{}");
            return pubpack.EAContext.strconv(ret,"gbk","utf-8");
            }
     sql="select mobile from usr where id='"+id+"'";
     ds=db.QuerySQL(sql);
    var data="";
    if( ds.getRowCount()>0 ) {
			data+=formatJsonDataByDS(ds);
		}else {
            var sql="select name from encode where id=5";
            var ds=db.QuerySQL(sql);
         	var tip=ds.getStringAt(0,0);
			ret=formatJsonVer(1,tip,"{\"tel\":\"\"}");
            return ret;
        }
        ret=formatJsonVer(1,"ok",data);

      return pubpack.EAContext.strconv(ret,"gbk","utf-8");
}
//查询该设备是否激活过
function QueryExistDeviceid(){
	var ret = formatJsonVer(1,"OK","{}");
	var db=DBConectSQL();
  	var deviceid = pubpack.EAFunc.NVL( request.getAttribute("deviceid"),"");
    var sql="select guid from act_code where deviceid='"+deviceid+"'";
    var ds=db.QuerySQL(sql);
    if( ds.getRowCount()>0 ) {
        var sql="select name from encode where id=4";
            var ds=db.QuerySQL(sql);
         	var tip=ds.getStringAt(0,0);
          	ret=formatJsonBool(1,tip,true);
        }else{
            var sql="select name from encode where id=3";
            var ds=db.QuerySQL(sql);
         	var tip=ds.getStringAt(0,0);
			ret=formatJsonBool(1,tip,false);
        }
      return ret;
}

//查询医院
function QueryHospital()
{
   	var ret = formatJsonVer(1,"OK","");
	var db=DBConectSQL();
    var sql="select id,name from con_hospital order by id";
    try{
    	var ds = db.QuerySQL(sql);
        var data="[";
		if( ds.getRowCount()>0 ) {
			data+=formatJsonDataByDS(ds);
		}else {
			ret=formatJsonVer(1,"医院信息为空为空!","[]");
            return pubpack.EAContext.strconv(ret,"gbk","utf-8");
        }
		data+="]";
        ret =  formatJsonVer(1,"ok",data);

    }catch(e){
        ret= formatJsonVer(-1,e.toString(),"");
    }
    return ret;
}
//新增医院
function NewConHospital(){
    var ret = formatJsonCode(1,"OK","");
	var db=DBConectSQL();
    var sql="";
    var name = pubpack.EAFunc.NVL( request.getAttribute("name"),"");
	var address = pubpack.EAFunc.NVL( request.getAttribute("address"),"");
    var region = pubpack.EAFunc.NVL( request.getAttribute("region"),"");
    var introduce = pubpack.EAFunc.NVL( request.getAttribute("introduce"),"");
    var tel = pubpack.EAFunc.NVL( request.getAttribute("tel"),"");
    var lev = pubpack.EAFunc.NVL( request.getAttribute("lev"),"");
    var bus_license = pubpack.EAFunc.NVL( request.getAttribute("bus_license"),"");
    var bus_permit = pubpack.EAFunc.NVL( request.getAttribute("bus_permit"),"");
    var cor_cer = pubpack.EAFunc.NVL( request.getAttribute("cor_cer"),"");
    var lev_prove = pubpack.EAFunc.NVL( request.getAttribute("lev_prove"),"");
    var cor_name = pubpack.EAFunc.NVL( request.getAttribute("cor_name"),"");
    var cor_phone = pubpack.EAFunc.NVL( request.getAttribute("cor_phone"),"");
    var cor_id = pubpack.EAFunc.NVL( request.getAttribute("cor_id"),"");
    var prinipal_name = pubpack.EAFunc.NVL( request.getAttribute("prinipal_name"),"");
    var prinipal_id = pubpack.EAFunc.NVL( request.getAttribute("prinipal_id"),"");
    var prinipal_email = pubpack.EAFunc.NVL( request.getAttribute("prinipal_email"),"");
    var prinipal_phone = pubpack.EAFunc.NVL( request.getAttribute("prinipal_phone"),"");
    if(name==""){
        ret=formatJsonCode(0,"医院名称不能为空","");
		return pubpack.EAContext.strconv(ret,"gbk","utf-8");
    }
    try{
        var	sql="select max(ID)+1 from CON_HOSPITAL";
        var ds = db.QuerySQL(sql);
        var newID=ds.getStringAt(0,0);
        sql="insert into CON_HOSPITAL(id,name,region,address,introduce,tel,lev,bus_license,bus_permit,cor_cer,lev_prove,cor_name,cor_phone,cor_id,prinipal_name,prinipal_id,prinipal_email,prinipal_phone)values('"+newID+"','"+name+"','"+region+"','"+address+"','"+introduce+"','"+tel+"','"+lev+"','"+bus_license+"','"+bus_permit+"','"+cor_cer+"','"+lev_prove+"','"+cor_name+"','"+cor_phone+"','"+cor_id+"','"+prinipal_name+"','"+prinipal_id+"','"+prinipal_email+"','"+prinipal_phone+"')";
        ret=formatJsonCode(1,"新增成功","");
        db.ExcecutSQL(sql);
        db.Commit();

    }catch(e){
        ret= formatJsonCode(-1,e.toString(),"");
    }
	return pubpack.EAContext.strconv(ret,"gbk","utf-8");
}
//机构（家庭）账户激活
function ActiveCode(){
	var ret = formatJsonCode(1,"OK","");
	var db=DBConectSQL();
	var mobile = pubpack.EAFunc.NVL( request.getAttribute("mobile"),"") ;
    var context = pubpack.EAFunc.NVL( request.getAttribute("context"),"") ;
    var active_code= pubpack.EAFunc.NVL( request.getAttribute("active_code"),"") ;
    var type= pubpack.EAFunc.NVL( request.getAttribute("type"),"") ;
    var name= pubpack.EAFunc.NVL( request.getAttribute("name"),"") ;
    var loc_id= pubpack.EAFunc.NVL( request.getAttribute("loc_id"),"") ;
	var password= pubpack.EAFunc.NVL( request.getAttribute("password"),"") ;
    var deviceId= pubpack.EAFunc.NVL( request.getAttribute("deviceId"),"") ;

    var codeds= pubpack.EAOption.msgRegisterCodeds;
   	var sult=getMSGCode(codeds,mobile);
   	if(sult=="-1"){
   	ret=formatJsonCode(0,"验证码过期！","");
   	}else if(context!=sult){
   	ret=formatJsonCode(0,"验证码错误！","");
   	}else{
    	try{
    	var sql="";
        var querySql="";
        var insSql="";
   		if(type=="1"){
        	sql="select name,guid from loc where id='"+loc_id+"'";
          	var ds = db.QuerySQL(sql);
            if(ds.getRowCount()<=0){
            	ret=formatJsonCode(0,"查询不到该机构","");
                return pubpack.EAContext.strconv(ret,"gbk","utf-8");
            }
            name=ds.getStringAt(0,0);
            var locguid=ds.getStringAt(0,1);
        	querySql="select count(1) from usr where id='"+loc_id+"'  and loctype=1";
        	sql="select count(1) from act_code where id='"+loc_id+"' and code='"+active_code+"' and available=1 and to_date(EXPIREDATE,'yyyy-mm-dd hh24:mi:ss')>=sysdate";
            insSql ="insert into usr(mobile,passwd,name,loctype,id,org,guid) values('"+mobile+"','"+password+"','"+name+"','1','"+loc_id+"','ry','"+locguid+"')";
        }else{
            querySql="select count(1) from usr where id='"+mobile+"' and loctype=2";
        	sql="select count(1) from act_code where  code='"+active_code+"' and id is null and available=1 and to_date(EXPIREDATE,'yyyy-mm-dd hh24:mi:ss')>=sysdate";
            insSql ="insert into usr(mobile,passwd,name,loctype,id,org) values('"+mobile+"','"+password+"','"+name+"','2','"+mobile+"','ry')";
        }
       	var ds = db.QuerySQL(querySql);
        //是否存在机构
        var nothaveloc=1;
        if(ds.getStringAt(0,0)>0){
        	nothaveloc=0;
        }else{
          var regexStr="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9*.@#$&]{8,}$";
    var p = regexpack.Pattern.compile(regexStr);
  	var m = p.matcher(password);
    if(!m.matches()){
    	return pubpack.EAContext.strconv(formatJsonCode(0,"密码必须包含大小写和数字，且8位及以上",""),"gbk","utf-8");
    }
        }
        //校验激活码是否有效
          	ds = db.QuerySQL(sql);
            if(ds.getStringAt(0,0)<=0){
                var sql="select name from encode where id=6";
            	var ds=db.QuerySQL(sql);
         		var tip=ds.getStringAt(0,0);

                ret=formatJsonCode(0,tip,"");
            }else{
            //	不存在该机构，则新建机构
            	if(nothaveloc==1){
                 db.ExcecutSQL(insSql);
                }
                //将激活码失效掉
                if(type==2){
                	sql="update act_code set id='"+mobile+"',available=0,deviceId='"+deviceId+"' where code='"+active_code+"'";
        			db.ExcecutSQL(sql);
                }else if(type==1){
                 	sql="update act_code set available=0 ,deviceId='"+deviceId+"' where code='"+active_code+"'";
        			db.ExcecutSQL(sql);
                }
        		db.Commit();
             ret=formatJsonCode(1,"ok","");
             }
            	return pubpack.EAContext.strconv(ret,"gbk","utf-8");

            }catch(e){
                        db.Rollback();

                    ret= formatJsonCode(-1,e.toString(),"");
            }finally{
                db.Close();
            }
   	}
	return pubpack.EAContext.strconv(ret,"gbk","utf-8");
}

//销售人员密码登陆
function salelogin()
{
	var ret = formatJsonlogin(1,"OK","","");
	var db=DBConectSQL();
	var usrid = pubpack.EAFunc.NVL( request.getAttribute("mobile"),"") ;
	var password= pubpack.EAFunc.NVL( request.getAttribute("password"),"") ;
    var regexStr="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9*.@#$&]{8,}$";
    var p = regexpack.Pattern.compile(regexStr);
  	var m = p.matcher(password);
    if(!m.matches()){
    	return pubpack.EAContext.strconv(formatJsonCode(0,"密码必须包含大小写和数字，且8位及以上",""),"gbk","utf-8");
    }
	var sql="select guid,id,name,passwd,mobile,refid from sales where  id='"+usrid+"'";
	var ds = db.QuerySQL(sql);
	if( ds.getRowCount()>0 ) {
		if(ds.getStringAt(0,"PASSWD")!=password){
			ret =  formatJsonlogin(-1,"密码错误","","");
		}else {
			var jwt=new pubpack.EAJwt();
			var token=jwt.createJWT(formatJsonDataByDS(ds));
			ret=formatJsonlogin(1,"OK",token,formatJsonDataByDS(ds));
        	return ret;
		}
	}
	else {
		ret= formatJsonlogin(0,"该用户不存在","","");
	}
	db.Close();
	return pubpack.EAContext.strconv(ret,"gbk","utf-8");
}

//用户密码登陆
function login()
{
	var ret = formatJsonlogin(1,"OK","","");
	var db=DBConectSQL();
	var usrid = pubpack.EAFunc.NVL( request.getAttribute("mobile"),"") ;
	var password= pubpack.EAFunc.NVL( request.getAttribute("password"),"") ;
    var deviceid = pubpack.EAFunc.NVL( request.getAttribute("deviceid"),"");
    var isnew= pubpack.EAFunc.NVL( request.getAttribute("isnew"),"");
        if(isnew=="1"){
            var sql="select guid from act_code where deviceid='"+deviceid+"'";
             var ds=db.QuerySQL(sql);
            if( ds.getRowCount()<=0 ) {
            var sql="select name from encode where id=3";
            var ds=db.QuerySQL(sql);
         	var tip=ds.getStringAt(0,0);
            ret=formatJsonlogin(-1,tip,"","");
            return ret;
            }
        }

	var sql="select guid,id,name,passwd,SEX,BIRTHDAY,IMGGUID,loctype,HID,DID from usr where  id='"+usrid+"' and org='ry'";
	var ds = db.QuerySQL(sql);
	if( ds.getRowCount()>0 ) {
		if(ds.getStringAt(0,"PASSWD")!=password){
			ret =  formatJsonlogin(-1,"密码错误","","");
		}else {
			var jwt=new pubpack.EAJwt();
			var token=jwt.createJWT(formatJsonDataByDS(ds));
			ret=formatJsonlogin(1,"OK",token,formatJsonDataByDS(ds));
        return ret;
		}
	}
	else {
		ret= formatJsonlogin(0,"该用户不存在","","");
	}
	db.Close();
	return ret;
}


//验证码登陆
function loginSMS()
{
	var ret = formatJsonlogin(1,"OK","","");
	var db=DBConectSQL();
	var usrid = pubpack.EAFunc.NVL( request.getAttribute("mobile"),"") ;
   var context= pubpack.EAFunc.NVL( request.getAttribute("context"),"") ;
        var sql="select mobile from usr where id='"+usrid+"'";
    var ds=db.QuerySQL(sql);
    if( ds.getRowCount()<=0 ) {
        sql="select guid from act_code where deviceid='"+deviceid+"'";
     ds=db.QuerySQL(sql);
      if( ds.getRowCount()<=0 ) {
        var sql="select name from encode where id=3";
        var ds=db.QuerySQL(sql);
        var tip=ds.getStringAt(0,0);
   		ret=formatJsonlogin(-1,tip,"","");
        return ret;

        }
		}
   var codeds= pubpack.EAOption.msgLoginCodeds;
   var sult=getMSGCode(codeds,usrid);
   if(sult=="-1"){
     	ret=formatJsonlogin(-1,"验证码过期","","");
   }else if(context==sult){
   		var sql="select guid,id,name,SEX,BIRTHDAY,IMGGUID from usr where  id='"+usrid+"' ";
      var ds = db.QuerySQL(sql);
      if( ds.getRowCount()>0 ) {
          var jwt=new pubpack.EAJwt();
          var token=jwt.createJWT(formatJsonDataByDS(ds));
          ret=formatJsonlogin(1,"OK",token,formatJsonDataByDS(ds));
          return ret;
      }
      else {
          ret= formatJsonlogin(0,"user not exist","","");
      }
   }else{
   		ret=formatJsonlogin(-1,"验证码错误！","","");
   }
	db.Close();
	return pubpack.EAContext.strconv(ret,"GBK","UTF-8");
}

//修改密码
function UpdatePasswordBySMS()
{
	var ret = formatJsonCode(1,"OK","");
	var db=DBConectSQL();
  	var guid = pubpack.EAFunc.NVL( request.getAttribute("guid"),"") ;
   	var context= pubpack.EAFunc.NVL( request.getAttribute("context"),"") ;
    var password= pubpack.EAFunc.NVL( request.getAttribute("password"),"") ;
    var regexStr="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9*.@#$&]{8,}$";
    var p = regexpack.Pattern.compile(regexStr);
  	var m = p.matcher(password);
    if(!m.matches()){
    	return pubpack.EAContext.strconv(formatJsonCode(0,"密码必须包含大小写和数字，且8位及以上",""),"gbk","utf-8");
    }
    //根据guid查询该手机号
    var sql="select mobile from usr where guid='"+guid+"'";
    var ds = db.QuerySQL(sql);
    if( ds.getRowCount()<=0 ) {
         return pubpack.EAContext.strconv(formatJsonCode(0,"该手机号不存在",""),"GBK","UTF-8");
    }
    var phone= ds.getStringAt(0,0);
   	var codeds= pubpack.EAOption.msgUpdatePasswd;
   	var sult=getMSGCode(codeds,phone);
   	if(sult=="-1"){
     	ret=formatJsonCode(0,"验证码过期！","","");
   	}else if(context==sult){
        sql	="update usr set passwd='"+password+"' where guid='"+guid+"'";
        db.ExcecutSQL(sql);
        db.Commit();
        ret=formatJsonCode(1,"修改密码成功","");

   	}else{
   		ret=formatJsonCode(0,"验证码错误！","");
   	}
	db.Close();
	return pubpack.EAContext.strconv(ret,"GBK","UTF-8");
}

//发送紧急呼叫短信
function SendSOSToContact(){
	var ret = formatJsonBool(1,"OK",true);
	var db=DBConectSQL();
    var crtguid = pubpack.EAFunc.NVL( request.getAttribute("crtguid"),"");
    var sql="SELECT ec.guid ,ec.name ,ec.phone,u.mobile FROM eme_contact  ec LEFT JOIN usr u ON ec.crtguid = u.guid  where ec.crtguid='"+crtguid+"' order by ec.crtdat";
    try{
    	var ds = db.QuerySQL(sql);
		if( ds.getRowCount()>0 ) {
        	//发送短信
            var url = "";
            var name="";
            var phone="";
            var sosMobile="";
            for(var i=0;i<ds.getRowCount();i++){
            	name=ds.getStringAt(i,1);
                phone= ds.getStringAt(i,2);
                sosMobile=ds.getStringAt(i,3);
                url="https://csth5.zijiapuzi.com/resource/sendSOS?phone="+phone+"&account="+sosMobile;
                itspack.HttpUtil.get(url);
            }
             // 提交请求
        	ret = formatJsonBool(1,"ok",true);
        }else {
        	ret = formatJsonBool(1,"联系人为空！",false);
              }
    }catch(e){
    	ret= formatJsonBool(-1,e.toString(),false);
    }
    return pubpack.EAContext.strconv(ret,"gbk","utf-8");
}

// 登陆，发送验证码到某个手机上
// 参数：phone
// 返回：smscode短信验证码
function sendSMS()
{
        var ret = formatJsonCode(1,"OK","");
        var db=DBConectSQL();
        var phone = pubpack.EAFunc.NVL( request.getAttribute("mobile"),"") ;
   			var type = pubpack.EAFunc.NVL( request.getAttribute("type"),"") ;
   			try{
            request.setCharacterEncoding("utf-8");
            //根据获取到的手机号发送验证码
            var smsCode = ((javapack.Math.random()*9+1)*100000)+"";
            smsCode=smsCode.substring(0,6);
            var url = "https://csth5.zijiapuzi.com/resource/sendCheckCode?phone="+phone+"&code="+smsCode;// 短信获取地址，需要填写，下面要参考短信发送地址的格式
             // 提交请求
            itspack.HttpUtil.get(url);
            var codeds=null;
            if(type=="1"){
            	codeds=pubpack.EAOption.msgRegisterCodeds;
            }else if(type=="2"){
            	codeds=pubpack.EAOption.msgLoginCodeds;
            }else if(type=="3"){
                codeds=pubpack.EAOption.msgUpdatePasswd;
            }

			return formatJsonCode(1,"OK",updateMSGCode(codeds,phone,smsCode));

        }catch(e){
				ret= formatJsonCode(-1,e.toString(),"");
        }
        return ret;

}

//医生注册
function RegisterDoctor()
{
        var ret = formatJsonCode(1,"OK","");
        var db=DBConectSQL();
        var phone = pubpack.EAFunc.NVL( request.getAttribute("mobile"),"") ;
        var password = pubpack.EAFunc.NVL( request.getAttribute("password"),"") ;
        var context = pubpack.EAFunc.NVL( request.getAttribute("context"),"") ;
        var name = pubpack.EAFunc.NVL( request.getAttribute("name"),"") ;
        var hid = pubpack.EAFunc.NVL( request.getAttribute("hid"),"") ;

        var codeds=pubpack.EAOption.msgRegisterCodeds;
        var regexStr="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9*.@#$&]{8,}$";
        var p = regexpack.Pattern.compile(regexStr);
   		var m = p.matcher(password);
    	if(!m.matches()){
    		return pubpack.EAContext.strconv(formatJsonCode(0,"密码必须包含大小写和数字，且8位及以上",""),"gbk","utf-8");
    	}
        try{
          var vercode=getMSGCode(codeds,phone);
          var sql="";
          if(vercode==context){
					 sql="select id,name from usr where id='"+phone+"'";
              var ds = db.QuerySQL(sql);
              if(ds.getRowCount()>0){
                  return formatJsonCode(0,pubpack.EAContext.strconv("该用户已存在","gbk","utf-8"),"");
              }else{
                sql="select 'a'||sys_guid() from dual";
                 ds=db.QuerySQL(sql);
            		var newguid=ds.getStringAt(0,0).substring(1);

                sql="insert into usr(newguid,org,id,name,passwd,mobile,hid) values('"+newguid+"','ry','"+phone+"','"+name+"','"+password+"','"+phone+"','"+hid+"')";
                db.ExcecutSQL(sql);
                sql="update con_hospital set crtguid='"+newguid+"' where id='"+hid+"' and crtguid is null ";
                db.ExcecutSQL(sql);

                db.Commit();
                return formatJsonCode(1,"OK","");
              }
          }else{
          	   return pubpack.EAContext.strconv(formatJsonCode(0,"验证码有错误",""),"GBK","UTF-8");
          }


        }catch(e){
        	db.Rollback();
			ret= formatJsonCode(-1,e.toString(),"");
        }
		return pubpack.EAContext.strconv(ret,"gbk","utf-8");

}
//注册
function Register()
{
        var ret = formatJsonCode(1,"OK","");
        var db=DBConectSQL();
        var phone = pubpack.EAFunc.NVL( request.getAttribute("mobile"),"") ;
        var password = pubpack.EAFunc.NVL( request.getAttribute("password"),"") ;
        var context = pubpack.EAFunc.NVL( request.getAttribute("context"),"") ;
        var name = pubpack.EAFunc.NVL( request.getAttribute("name"),"") ;

        var codeds=pubpack.EAOption.msgRegisterCodeds;
        var regexStr="^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9*.@#$&]{8,}$";
        var p = regexpack.Pattern.compile(regexStr);
   		var m = p.matcher(password);
    	if(!m.matches()){
    		return pubpack.EAContext.strconv(formatJsonCode(0,"密码必须包含大小写和数字，且8位及以上",""),"gbk","utf-8");
    	}
        try{
          var vercode=getMSGCode(codeds,phone);
          var sql="";
          if(vercode==context){
					 sql="select id,name from usr where id='"+phone+"'";
              var ds = db.QuerySQL(sql);
              if(ds.getRowCount()>0){
                  return formatJsonCode(0,pubpack.EAContext.strconv("该用户已存在","gbk","utf-8"),"");
              }else{
                sql="select 'a'||sys_guid() from dual";
                 ds=db.QuerySQL(sql);
            		var newguid=ds.getStringAt(0,0).substring(1);

                sql="insert into usr(guid,org,id,name,passwd,mobile) values('"+newguid+"','ry','"+phone+"','"+name+"','"+password+"','"+phone+"')";
                db.ExcecutSQL(sql);

                //默认添加普通服务包
                // sql="insert into locsrv(usrguid,usrname,srvid,srvname) select '"+newguid+"','"+name+"',id,name from srvpack where ord_lev='1'";
                // db.ExcecutSQL(sql);
                db.Commit();
                return formatJsonCode(1,"OK","");
              }
          }else{
          	   return pubpack.EAContext.strconv(formatJsonCode(0,"验证码有错误",""),"GBK","UTF-8");
          }


        }catch(e){
        		db.Rollback();
				ret= formatJsonCode(-1,e.toString(),"");
        }
		return pubpack.EAContext.strconv(ret,"gbk","utf-8");

}



// updateMSGCode(pubpack.EAOption.msgLoginCodeds,"123400000","124553");更新登陆短信验证码到缓冲
// updateMSGCode(pubpack.EAOption.msgRegisterCodeds,"123400000","124553");更新注册短信验证码到缓冲
function updateMSGCode(ds,phone,code)
{
  // PHONE CODE DATTIM
  // find
  var vercode="";
  var bFind = false;
  for ( var i=0;i<ds.getRowCount();i++){
    if(ds.getStringAt(i,"PHONE")== phone){
    //return ds.getStringAt(i,"PHONE")+","+pubpack.EAFunc.GetLatestTimeStr()+","+phone;
      ds.setValueAt(i,"DATTIM",pubpack.EAFunc.GetLatestTimeStr());
      ds.setValueAt(i,"CODE",code );
      vercode=ds.getStringAt(i,"CODE");
      bFind = true;
      break;
 	 }
  }
  if(bFind==false){
    // new
    var row=ds.getRowCount();
	  ds.AddNullRow(row-1);
    ds.setValueAt(row,"PHONE",phone);
    ds.setValueAt(row,"DATTIM",pubpack.EAFunc.GetLatestTimeStr());
    ds.setValueAt(row,"CODE",code);
    vercode=code;
  }
  return vercode;
}


// getMSGCode(pubpack.EAOption.msgLoginCodeds,"123400000");从缓冲获取登陆短信验证码到
// getMSGCode(pubpack.EAOption.msgRegisterCodeds,"123400000");//从缓冲获取注册短信验证码
function getMSGCode(ds,phone){
   // PHONE CODE DATTIM
   // find
   try{
   	  if(ds.getRowCount()>0){
        for ( var i=0;i<ds.getRowCount();i++){
          if(ds.getStringAt(i,"PHONE")== phone){
              var fdate=ds.getStringAt(i,"DATTIM");
              var tdate=pubpack.EAFunc.GetLatestTimeStr();
              if(pubpack.EAFunc.TimeDifference(fdate,tdate)/(1000*60)>15){
                  return "-1";
              }else{
                  return ds.getValueAt(i,"CODE" );
              }
          }
        }

     }

     return "";


   }catch(e){
		return e.toString();
  }

}

//注册
function NewPatient()
{
       var ret = formatJsonCode(1,"OK","");
        var db=DBConectSQL();
        var name = pubpack.EAFunc.NVL( request.getAttribute("name"),"") ;
        var sex = pubpack.EAFunc.NVL( request.getAttribute("sex"),"") ;
        var phone = pubpack.EAFunc.NVL( request.getAttribute("phone"),"") ;
        var idcard = pubpack.EAFunc.NVL( request.getAttribute("idcard"),"") ;
        try{
          if(phone!=""){
					 sql="select name from patient where mobtle='"+phone+"'";
              var ds = db.QuerySQL(sql);
             if(ds.getRowCount()>0){
                  ret=formatJsonCode(2,"该用户已经存在","");
              }else{
                sql="insert into patient(name,sex,mobtle,idcard) values('"+name+"','"+sex+"','"+phone+"','"+idcard+"')";
                db.ExcecutSQL(sql);
                db.Commit();
                ret=formatJsonCode(1,"新增成功","");
              }
          }else{
          		ret=formatJsonCode(-1,"手机号不能为空","");

          }


        }catch(e){
				ret= formatJson(-1,e.toString(),"");
        }
			return pubpack.EAContext.strconv(ret,"gbk","utf-8");
}

//版本升级
function version()
{
        var ret = formatJsonVer(0,"OK","{}");
        var db=DBConectSQL();
        var id = pubpack.EAFunc.NVL( request.getAttribute("id"),"") ;
        var name = pubpack.EAFunc.NVL( request.getAttribute("name"),"") ;
        //var remarks = pubpack.EAFunc.NVL( request.getAttribute("remarks"),"") ;
        var sql="";
        try{
          if(id!=""&&name!=""){
					 sql="select id,remarks from VERSIONUPDATE where name='"+name+"' and org='ry'";
              var ds = db.QuerySQL(sql);
             if(ds.getRowCount()>0){
                 var qid=ds.getStringAt(0,"ID");
                 if(id<qid){
                 	sql="select id,url,remarks from VERSIONUPDATE where name='"+name+"' and org='ry'";
                   ds =db.QuerySQL(sql);
                   ret=formatJsonVer(1,"OK",formatJsonDataByDS(ds));
                  }
              }
          }else{
          		pubpack.EAContext.strconv(formatJsonVer(0,"版本号和名称不能为空","{}"),"gbk","utf-8");

          }


        }catch(e){
				ret= formatJson(-1,e.toString(),"");
        }
			return ret;
}

//修改版本号
function versionupdate()
{
        var ret = formatJsonVer(0,"","{}");
        var db=DBConectSQL();
        var id = pubpack.EAFunc.NVL( request.getAttribute("id"),"") ;
        var name = pubpack.EAFunc.NVL( request.getAttribute("name"),"") ;
        var sql="";
        try{
          if(id!=""){
					 sql="select id from VERSIONUPDATE where name='"+name+"' and org='ry'";
              var ds = db.QuerySQL(sql);
             if(ds.getRowCount()>0){
                 sql="update VERSIONUPDATE set id='"+id+"' where name='"+name+"' and org='ry'";
                 db.ExcecutSQL(sql);
                 ret=formatJsonVer(1,"ok","{}");

              }else{
              		sql="insert into VERSIONUPDATE(org,id,name) values ('ry','"+id+"','"+name+"')";
                 db.ExcecutSQL(sql);
                 ret=formatJsonVer(1,"ok","{}");
              }
              db.Commit();
          }else{
          		ret=formatJsonVer(-1,"版本号和名称不能为空","{}");

          }

        }catch(e){
				ret= formatJsonVer(-1,e.toString(),"{}");
        }
			return pubpack.EAContext.strconv(ret,"gbk","utf-8");
}
//EAFunc.java
// static EADS qrloginds =new EADS();
//  EAFunc.qrloginds
// 二维码登录，查询某个id的状态
// function qrcodeloginquery() {
// 	var ret = formatJsonVer(0,"","{}");
//    var db=DBConectSQL();
//    var usrid = pubpack.EAFunc.NVL( request.getParameter("usrid"),"");
//    var sql ="";
//    try{
//       sql = "select id,name from qrcode where usrid='"+usrid+"' and stat='1'";
//       var ds=db.QuerySQL(sql);
//       if(ds.getRowCount()>0){
//       		ret=formatJsonVer(1,"OK",formatJsonDataByDS(ds));
//       		sql = "delete from qrcode where usrid='"+usrid+"' and stat='1'";
//          db.ExcecutSQL(sql);
//          db.Commit();
//       }else{
//       		ret=formatJsonVer(0,"","{}");
//       }

//     }catch(e){
//       ret= formatJsonVer(-1,e.toString(),"{}");
//     }
//     db.Close();
//     return ret;
// }
// 二维码登录：更改某id的状态为1
// function qrcodeloginupdate() {

// 	var ret = formatJsonCode(0,"","");
//    var db=DBConectSQL();
//    var id = pubpack.EAFunc.NVL( request.getParameter("unionid"),"");
//    var nickname = pubpack.EAFunc.NVL( request.getParameter("nickname"),"");
//    var usrid = pubpack.EAFunc.NVL( request.getParameter("usrid"),"");
//    var sql="";
//    try{
//       sql = "select id,name from qrcode where id='"+id+"'";
//       var ds=db.QuerySQL(sql);

//       if(ds.getRowCount()>0){
//       		sql = "update qrcode set stat='1' where id='"+id+"'";
//          db.ExcecutSQL(sql);
//          ret=formatJsonCode(1,"OK","");
//       }else{
//       		sql = "insert into qrcode(id,stat,name,usrid) values('"+id+"','1','"+nickname+"','"+usrid+"')";

//          db.ExcecutSQL(sql);
//       		ret=formatJsonCode(1,"OK","");
//       }
//        db.Commit();
//     }catch(e){
//       ret= formatJsonCode(-1,e.toString(),"");
//     }
//     db.Close();
//     return ret;

// }


function formatJsonlogin(code,msg,token,data)
{
	var jsonstr =  "{\"code\":\""+code+"\",\"message\":\""+msg+"\",\"data\":{\"ds\":[";
	jsonstr+=data;
	jsonstr+="],\"token\":\""+token+"\"}}";
	return jsonstr;
}
function formatJsonVer(code,msg,data)
{
	var jsonstr =  "{\"code\":\""+code+"\",\"message\":\""+msg+"\",\"data\":";
	jsonstr+=data;
	jsonstr+="}";
	return jsonstr;
}
function formatJsonCode(code,msg,data)
{
	var jsonstr =  "{\"code\":\""+code+"\",\"message\":\""+msg+"\"}";
	return jsonstr;
}
function formatJson(code,msg,data)
{
	var jsonstr =  "{\"code\":\""+code+"\",\"message\":\""+msg+"\",\"data\":[";
	jsonstr+=data;
	jsonstr+="]}";
	return jsonstr;
}
function formatJsonBool(code,msg,bool)
{
	var jsonstr =  "{\"code\":\""+code+"\",\"message\":\""+msg+"\",\"result\":";
	jsonstr+=bool;
	jsonstr+="}";
	return jsonstr;
}
function formatJsonDataByDS(ds)
{
	var data = "";
	for ( var i=0;i<ds.getRowCount();i++){
		if( i>0) data+=",";
		data+="{";
			for ( var j=0;j<ds.getColumnCount();j++){
				var colnam = ds.getColumnName(j);
				if(j>0) data+=",";
				data+="\""+colnam+"\":\""+ds.getStringAt(i,j)+"\" ";
			}
		data+="}";
	}
	return data;
}
function DBConectSQL()
{
		var db = new pubpack.EADatabase("jdbc:oracle:thin:@smartcolink.com:1521:XE","ry","Eru43wPo","oracle.jdbc.driver.OracleDriver");
		return db;
}