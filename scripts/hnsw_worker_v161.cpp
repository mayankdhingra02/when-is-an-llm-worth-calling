// Original benchmark adapter; hnswlib v0.8.0 is Apache-2.0, unmodified.
#include "hnswlib/hnswlib.h"
#include <chrono>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <thread>
#include <vector>
#include <atomic>
#include <stdexcept>
int main(int argc,char**argv) {
 try {
  if(argc!=8) throw std::runtime_error("train query output M ef_construction ef_search threads");
  const size_t n=3823,nq=1797,dim=64,k=10;
  int M=std::stoi(argv[4]),efc=std::stoi(argv[5]),efs=std::stoi(argv[6]),nt=std::stoi(argv[7]);
  if(M<4||M>32||efc<32||efc>128||efs<10||efs>256||nt<1||nt>4)throw std::runtime_error("argument bounds");
  std::vector<float> train(n*dim),query(nq*dim);
  for(auto pair:{std::make_pair(argv[1],&train),std::make_pair(argv[2],&query)}) {
   std::ifstream in(pair.first,std::ios::binary);if(!in.read(reinterpret_cast<char*>(pair.second->data()),pair.second->size()*sizeof(float))||in.peek()!=EOF)throw std::runtime_error("input size");
  }
  std::vector<size_t> ids(nq*k);std::atomic<size_t> next{0};
  hnswlib::L2Space space(dim);
  auto start=std::chrono::steady_clock::now();
  hnswlib::HierarchicalNSW<float> index(&space,n,M,efc,100);
  for(size_t i=0;i<n;i++)index.addPoint(train.data()+i*dim,i);
  index.setEf(efs);
  auto built=std::chrono::steady_clock::now();
  auto work=[&](){for(size_t j=next.fetch_add(1);j<nq;j=next.fetch_add(1)) {
   auto out=index.searchKnn(query.data()+j*dim,k);if(out.size()!=k)std::terminate();
   for(size_t z=0;z<k;z++){ids[j*k+z]=out.top().second;out.pop();}
  }};
  std::vector<std::thread> workers;for(int i=0;i<nt;i++)workers.emplace_back(work);
  for(auto&t:workers)t.join();
  auto end=std::chrono::steady_clock::now();
  std::ofstream output(argv[3]);for(size_t j=0;j<nq;j++){for(size_t z=0;z<k;z++)output<<(z?" ":"")<<ids[j*k+z];output<<"\n";}
  if(!output.good())throw std::runtime_error("output failure");
  std::cout<<std::setprecision(17)<<"{\"build_seconds\":"<<std::chrono::duration<double>(built-start).count()<<",\"query_seconds\":"<<std::chrono::duration<double>(end-built).count()<<",\"objective_seconds\":"<<std::chrono::duration<double>(end-start).count()<<",\"indexed\":"<<n<<",\"queries\":"<<nq<<",\"k\":"<<k<<",\"build_threads\":1,\"query_threads\":"<<nt<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}
}
