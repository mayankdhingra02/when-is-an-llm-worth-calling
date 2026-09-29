import java.sql.*;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;

/** Own benchmark harness; H2 is an unmodified registry dependency. */
public class H2Probe {
  static final int N=100000, PARAMS=16, ROUNDS=4;
  static final String[] SQL={
    "SELECT COUNT(*), COALESCE(SUM(amount),0) FROM events WHERE grp=? AND score BETWEEN ? AND ?",
    "SELECT COUNT(*), COALESCE(SUM(amount),0) FROM events WHERE acct=? AND grp=?",
    "SELECT COUNT(*), COALESCE(SUM(amount),0) FROM events WHERE tick>=? AND tick<?"};
  static final String[] COLS={"grp","acct","score","grp,score","acct,grp","tick"};
  static void bind(PreparedStatement p,int q,int t) throws Exception {
    if(q==0){int low=t*431%9000;p.setInt(1,t*7%97);p.setInt(2,low);p.setInt(3,low+500);}
    else if(q==1){p.setInt(1,t*43%997);p.setInt(2,t*11%97);}
    else {int low=t*5701%90000;p.setInt(1,low);p.setInt(2,low+1000);}
  }
  static long[][] truth(){
    long[][] a=new long[48][2];
    for(int i=0;i<N;i++)for(int t=0;t<PARAMS;t++){
      int g=i*37%97,account=i*29%997,score=i*13%10000;long amount=(long)i*7919%100000;
      int low=t*431%9000;
      if(g==t*7%97 && score>=low && score<=low+500){a[t][0]++;a[t][1]+=amount;}
      if(account==t*43%997 && g==t*11%97){a[16+t][0]++;a[16+t][1]+=amount;}
      low=t*5701%90000;if(i>=low && i<low+1000){a[32+t][0]++;a[32+t][1]+=amount;}
    }
    return a;
  }
  static void suite(PreparedStatement[] ps,long[][] expected,StringBuilder output,int round) throws Exception {
    for(int q=0;q<3;q++)for(int t=0;t<PARAMS;t++){
      bind(ps[q],q,t);
      try(ResultSet r=ps[q].executeQuery()){
        if(!r.next())throw new AssertionError("Missing result");long count=r.getLong(1),sum=r.getLong(2);
        if(r.next() || count!=expected[q*16+t][0] || sum!=expected[q*16+t][1])throw new AssertionError("Incorrect SQL result "+q+"/"+t);
        if(output!=null)output.append(round+","+q+","+t+","+count+","+sum+"\n");
      }
    }
  }
  public static void main(String[] args) throws Exception {
    int mask=Integer.parseInt(args[0]),sample=Integer.parseInt(args[2]);boolean recompile=Boolean.parseBoolean(args[1]);
    if(mask<0 || mask>63 || Integer.bitCount(mask)>3 || !(sample==0||sample==100||sample==2000||sample==10000))throw new IllegalArgumentException();
    Path out=Path.of(args[3]);Files.createDirectories(out);long start=System.nanoTime();long[][] expected=truth();
    String url="jdbc:h2:mem:v82;QUERY_CACHE_SIZE=8;RECOMPILE_ALWAYS="+recompile+";ANALYZE_AUTO=0";
    try(Connection c=DriverManager.getConnection(url,"sa","");Statement s=c.createStatement()){
      if(!c.getMetaData().getDatabaseProductVersion().startsWith("2.3.232"))throw new AssertionError("Version mismatch");
      s.execute("SET OPTIMIZE_REUSE_RESULTS FALSE");
      s.execute("CREATE TABLE events(id INT PRIMARY KEY, grp INT, acct INT, score INT, tick INT, amount BIGINT)");
      s.execute("INSERT INTO events SELECT X, MOD(X*37,97), MOD(X*29,997), MOD(X*13,10000), X, MOD(X*CAST(7919 AS BIGINT),100000) FROM SYSTEM_RANGE(0,99999)");
      long indexStart=System.nanoTime();
      for(int i=0;i<6;i++)if((mask&(1<<i))!=0)s.execute("CREATE INDEX idx"+i+" ON events("+COLS[i]+")");
      if(sample>0)s.execute("ANALYZE TABLE events SAMPLE_SIZE "+sample);
      long indexEnd=System.nanoTime();
      StringBuilder settings=new StringBuilder();
      try(ResultSet r=s.executeQuery("SELECT SETTING_NAME,SETTING_VALUE FROM INFORMATION_SCHEMA.SETTINGS WHERE SETTING_NAME IN ('RECOMPILE_ALWAYS','QUERY_CACHE_SIZE','ANALYZE_AUTO','OPTIMIZE_REUSE_RESULTS') ORDER BY SETTING_NAME")){
        while(r.next())settings.append(r.getString(1)+"="+r.getString(2)+"\n");
      }
      boolean reuse=((org.h2.engine.SessionLocal)((org.h2.jdbc.JdbcConnection)c).getSession()).getDatabase().getOptimizeReuseResults();
      if(reuse)throw new AssertionError("Result reuse enabled");
      settings.append("OPTIMIZE_REUSE_RESULTS_ENGINE="+reuse+"\n");
      Files.writeString(out.resolve("settings.txt"),settings.toString());
      StringBuilder indexes=new StringBuilder();
      try(ResultSet r=s.executeQuery("SELECT INDEX_NAME,COLUMN_NAME,ORDINAL_POSITION FROM INFORMATION_SCHEMA.INDEX_COLUMNS WHERE TABLE_NAME='EVENTS' ORDER BY INDEX_NAME,ORDINAL_POSITION")){
        while(r.next())indexes.append(r.getString(1)+","+r.getString(2)+","+r.getInt(3)+"\n");
      }
      Files.writeString(out.resolve("indexes.csv"),indexes.toString());
      PreparedStatement[] ps=new PreparedStatement[3];for(int q=0;q<3;q++)ps[q]=c.prepareStatement(SQL[q]);
      suite(ps,expected,null,-1); // fixed unscored warm-up, included in collected process cost
      StringBuilder answer=new StringBuilder("round,query,parameter,count,sum\n");
      long queryStart=System.nanoTime();for(int round=0;round<ROUNDS;round++)suite(ps,expected,answer,round);long queryEnd=System.nanoTime();
      Files.writeString(out.resolve("answers.csv"),answer.toString(),StandardCharsets.UTF_8);
      for(PreparedStatement p:ps)p.close();
      String result="{\"version\":\"2.3.232\",\"rows\":"+N+",\"scored_queries\":192,\"warmup_queries\":48,\"mask\":"+mask+",\"recompile\":"+recompile+",\"analyze_sample\":"+sample+",\"query_seconds\":"+((queryEnd-queryStart)/1e9)+",\"index_and_analyze_seconds\":"+((indexEnd-indexStart)/1e9)+",\"harness_seconds\":"+((System.nanoTime()-start)/1e9)+"}";
      Files.writeString(out.resolve("metrics.json"),result+"\n");System.out.println(result);
    }
  }
}
