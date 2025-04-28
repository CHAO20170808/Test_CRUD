/// <reference types="cypress" />
 
describe('API testing',function(){
 
    it('GET Method',function(){
        cy.request('GET','http://127.0.0.1:5000/read').then((response)=>{
            expect(response.status).equal(200)
            ///print(response.body.data)
            console.log(response.body);
            //expect(response.body.data[8][1]).equal('Product 7')
           // 驗證第 8 筆（索引為 8）的第二個元素是否為 "Product 7"
            expect(response.body[8][1]).to.equal('Product 7');
        })
    })
 
    xit('POST Method',function(){
        var user={
            "name": "guest",
            "price": 98.25
        }
        cy.request('POST','http://127.0.0.1:5000/create',user).then((response)=>{
            expect(response.status).equal(200);
/*             // 檢查資料是否包含新增的項目
        const isDataPresent = Array.isArray(response.body) && response.body.some((item) => {
        return item[1] === user.name && item[2] === user.price;
       });

        expect(isDataPresent).to.be.true; */

      // 確認回應資料是否為陣列
      expect(Array.isArray(response.body)).to.be.true;

      // 檢查新增資料是否存在於回應中
      const isDataPresent = response.body.some((item) => {
        return item[1] === user.name && item[2] === user.price;
      });

      // 驗證新增資料是否正確
      expect(isDataPresent).to.be.true;


         })
    })


 
    xit('PUT Method',function(){
        var user={
            "name": "vignesh",
            "price": 3588
        }
        cy.request('PUT','http://127.0.0.1:5000/update/69',user).then((response)=>{
            expect(response.status).equal(200)
            console.log(response.body);
            expect(response.body[42][1]).to.equal(user.name)
            expect(response.body[42][2]).to.equal(user.price)
        })
    })
 
    it('DELETE Method',function(){
        cy.request('DELETE','http://127.0.0.1:5000/delete/69').then((response)=>{
            expect(response.status).equal(200)
        })
    })
 
 
})