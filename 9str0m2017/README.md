Đề bài là 1 file exe 32bit, ẩn trong đó là flag của 3 level cần tìm.
### Level 1
Mở file đề bài cho, mình mò mẫm ở GUI, Check, Donate thử đều báo Invaild.
Tiếp tục mở thử hộp thoại About Us thì có ngay flag của level1 như thế này:

![Imgur](https://i.imgur.com/8zVWGKH.png)

Xem code thì thấy rằng nếu input nhập vào có 16 kí tự và các kí tự của input khi xor với 1 thì sẽ ra được flag đúng.
Vậy thì ta chỉ cần xor lại chuỗi ở trên với 1 là ra flag bài đầu tiên: ![level1](https://github.com/hongsonars/mywriteups/blob/master/9str0m2017/level1.py)
### Level 2
Level 2 khá khó khi so với level1.
Vì 3 challenge đều chung 1 file nên, đầu tiên, phải tìm xem lấy flag của level2 ở chỗ nào đã.
Qua level 1 thì thấy lúc hiện flag thì sẽ có dạng "The flag of levelx is:..." nên mình vào trong HxD, tìm chuỗi level2 thì thấy nó nằm gần gần chỗ "Your wallet is invalid". Mà cái chuỗi này hiện ra khi bấm vào nút Check. Vì vậy để lấy được flag của level2 có lẽ là phải input cái gì đó rồi Check. Đúng thì được flag còn sai thì badboy "Your wallet is invalid" nhảy ra thay cho flag.
Còn lại "Donate" chắc là của level 3 để xem sau vậy.
Mở x32dbg lên, tìm các chuỗi liên quan thì thấy gần chỗ call MessageBox ra badboy có hàm GetDlgTextItem có vẻ là hàm lấy input. F2 đặt Breakpoint tại đấy rồi nhập input :arrow_right: chương trình dừng ngay tại hàm này. Bắt đầu trace từ đây để tìm flag.

[GetDlgTextItem](https://msdn.microsoft.com/en-us/library/windows/desktop/ms645489v=vs.85.aspx) nhận vào 4 tham số trong đó tham số thứ 3*lpString* là địa chỉ buffer nhận input, và thứ 4 *nMaxCount* là số byte tối đa của input. Các tham số được truyền theo thứ tự từ phải sang trái nên có thể thấy [ebp-E8] là địa chỉ nhận input và 0x19 == 25 là số byte tối đa có thể nhận. Hàm sẽ trả về số byte đã đọc vào buffer về eax.
Đoạn code tiếp theo sau khi gọi hàm GetDlgTexItem:

![Imgur](https://i.imgur.com/IG5MnoK.png)

Có thể hiểu như sau:
* Nếu số byte đã đọc bằng 0 thì nhảy ra badboy.
* Đọc lần lượt các byte của input được lưu ở [ebp-E8] rồi đếm số byte đã đọc lưu vào địa chỉ [ebp-664]
* So sánh số byte đó với 0x18 == 24. Nếu bằng nhau sẽ pass được badboy đầu tiên. :arrow_right: Input có 24byte.
Tiếp tục đến đây:

![Imgur](https://i.imgur.com/3V6ijwu.png)

* Lần lượt 4 byte đầu tiên(dword ptr[ebp-E8]) và 4byte tiếp theo [dword ptr [ebp-E4] của in put đc copy vào [ebp-15C] và [ebp - 158] :arrow_right: [ebp-15C] trỏ đến 8bytes đầu tiên của input.
* Hàm 0x402570 được gọi với tham số là buffer chứa 8bytes input đầu và địa chỉ buffer [ebp-140] - có thể là địa chỉ để lưu trữ kết quả sau khi  xử lí 8bytes đầu kia.

Vào thử hàm 00xx402570 này, thấy nó lằng nhằng quá, lại còn gọi thêm hàm 0x402640 nữa nên biếng quá vào bật Ida thần thánh lên soi thử:

![Imgur](https://i.imgur.com/FOhBUYB.png)

Tiếp tục soi hàm tại đc 0x402640:

![Imgur](https://i.imgur.com/k4vbzyK.png)

byte_43E000 = "0123456789+/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

Đại khái là hàm 0x402570 được gọi để xử lí 8byte đầu tiên trong input. Và cứ 3byte thì lại được xử lí ra 4 kí tự. Nếu thiếu thì sẽ được add thêm byte 0x61 ('=') vào cuối cho đủ 4 kí tự. 8byte :arrow_right: có 3 lần đc xử lí, vì lần cuối chỉ có 2byte nên chuỗi sau khi xử lí sẽ có dấu '=' ở cuối. :arrow_right: chuỗi sau khi xử lí có 12byte được lưu vào [ebp-140].

Nhìn qua có vẻ giống base64 vì cũng thường có byte cuối là dấu '=' nhưng decode không được, nên mình nghĩ là dấu '=' được thêm vào cho nó nguy hiểm, đánh lừa người chơi :expressionless:. (Nhưng thực tế thì nó là base64 với custom charset, cơ mà mình méo biết vì k đọc về mã hóa của base64 bao giờ. Hôm trước có hỏi 1 anh ở trường mình mới biết được điều này).

Quay lại x64dbg thì thấy sau khi xử lí xong 8byte đó, kết quả lưu tại [ebp-140] sẽ được so sánh lần lượt từng byte 1 với chuỗi tại [ebp-668] = "olCOkyDvq7i=". Sai byte nào thì ra badbadboy luôn.
Đến đây cũng khá khoai với mình khi phải tìm chuỗi sau khi xử lí ra được chuôi "olCO.." kia(do trước mình chưa biết là base64 custom charset, giờ thì được thông rồi :smile:), nhưng may mắn là dạng này đã gặp 1 lần rồi + 1 lần xem ở kênh ![GynvaelEN]("https://www.youtube.com/channel/UCCkVMojdBWS-JtH7TliWkVg") có dùng z3py để solve 1 challenge nên mềnh cũng học được tí(lần đó thấy z3 nó cũng thần thánh chả kém gì cái decompiler của ida :smile:, cũng viết được 1 cái script để tính ra 8byte đầu của input. (Cách này khá hên xui, có bài ra có bài không ra.)
> input1 = "iz4ZJapu"


Còn tới 16byte nữa, khoai quá :worried:
Qua block 1 sẽ đến hàm gọi hàm kiểm tra *IsDebuggerPresent*. Hàm này trả về giá trị = 0 khi không có debuger, và != 0 khi phát hiện debuger.
Sau đó kiểm tra eax nếu = 0 thì ra badboy. Wtf?? như vậy là phải chạy trong debuger mới được à :expressionless: chắc có gì nhầm lẫn ở đây :expressionless: đang dùng debuger nên để vậy đã, có gì sau này patch lại thành ```mov eax, 1``` là xong.

![Imgur](https://i.imgur.com/gCeGgCf.png)

Chương trình tiếp tục lưu các byte đã đọc vào [ebp-124]. Số byte đã đọc được lưu [ebp-618] rồi so sánh với 0x10 == 16.
Còn nhớ là [ebp-E8] là địa chỉ trỏ tới byte đầu tiên trong input vậy nên khi lệnh movsx edx, byte ptr ss:[ebp+ecx-E8](với ecx đc gán = số byte đã đọc) thực thi thì edx sẽ nhận byte input thứ 9(vì trước đó đọc 8byte òi).
edx sau đó sẽ được xor với từng byte trong chuỗi được lưu ở [ebp-670] = "khangkit" và kết quả của phép xor được lưu vào đchỉ [ebp-140].
Việc này lặp lại cho đến khi đọc được 16byte, tức là đọc xong 8byte tiếp theo.
Sau đó hàm tại 0x404000 được gọi với 3 tham số theo thứ tự là [ebp-30], [ebp-140], 8.
Sau khi hàm này thực hiện xong, kết quả được trả về eax.  Lại thấy cái hàm này phức tạp, mò vào ida xem thử:

![Imgur](https://i.imgur.com/l50nfXr.png)

Có 6 case tương ứng từ 0->4 và default mà a3 được truyền vào là 8 :arrow_right: hàm sub_4041C0 được gọi để xử lý 3 tham số truyền vào. Để ý sau đó thì giá trị trả về được so sánh nếu = 0 thì nhảy qua đc badboyt. Tiếp tục F5 :smiling_imp:

Kinh vãi, hơn 200 dòng :scream:. Nhưng để ý thì vẫn là switch(a3==8). Với v44 = a1+a3 và v45 = a2+a3 thì lúc này hàm  sub_403E80 vẫn chỉ đang xử lí 2 cái chuỗi được truyền vào.

![Imgur](https://i.imgur.com/TiK3oXI.png)
![Imgur](https://i.imgur.com/VVz15um.png)

Hàm sub_403E80 sẽ trả về 0 - là đúng(giá trị trả về khác với khi kiểm tra. Cái này hơi lằng nhằng, hàm trả về True = 0, còn False = !=0. Còn khi so sánh trong if() hoặc while() thì !=0 ==True,) khi giá trị byte tại tham số nhận vào = nhau. Khi v19 = 0 sẽ gọi tiếp hàm sub_403E80 với 4 byte còn lại.
Suy cho cùng thì là so sánh từng byte của 2 chuỗi [ebp-30] và [ebp-140] với nhau :expressionless: . Nếu 2 chuỗi bằng nhau sẽ trả về 0, khác nhau sẽ trả về kết quả != 0. Thực tế là mình đoán luôn đây là hàm so sánh 2 chuỗi byte vì 1 hàm nhận 2 chuỗi và kết quả trả về đc so sánh với 0 thì sẽ là hàm so sánh 2 chuỗi byte đó. Khi làm thấy sai mới mò tiếp :smile:
Ok vậy là để qua được block tiếp theo thì input nhập vào sau khi xor từng byte với chuỗi "khangkit" phải ra kết quả như ở đchỉ [ebp-30]. Để tính input thì chỉ cần xor ngược lại [ebp-30] và "khangkit" là xong.

8byte đúng tiếp theo lại được copy tiếp  sang [ebp-124]. Hàm GetLocalTime này thì dễ hiểu hơn. Lưu  ngày giờ hiện tại theo struct ![SYSTEMTIME](https://msdn.microsoft.com/en-us/library/windows/desktop/ms724950.aspx) vào [ebp-610] và ghi 4 lần dạng nguyên(%d) của giờ vào địa chỉ tại [epb-1F8]. So sánh luôn với chuỗi tại 0x42E618 = "12121212". 

![Imgur](https://i.imgur.com/tlui5Zv.png)

 :arrow_right: GetLocalTime được 12p.m thì sẽ qua được bước này. Ở đây mình patch lại luôn hàm call ![GetLocalTime](https://msdn.microsoft.com/en-us/library/windows/desktop/ms724338(v=vs.85).aspx) thành ```mov byte ptr [eax+8], 0xc```([eax+8] là vị trí lưu giờ trong struct SYSTEMTIME) để lúc nào cũng ghi 12 vào [ebp-1F8].

Tiếp tục nốt phần còn lại:

![Imgur](https://i.imgur.com/GLbG4Tu.png)

Tương đối giống với block thứ 2 vừa xử xong. Chương trình cũng đọc lần lượt các byte còn lại cho đến hết(cmp với 0x18 = 24). Đưa số 8 byte còn lại vào edx, ecx được gán lần lượt bởi chuỗi trỏ bởi [ebp-1F8] - "12121212". Xor chúng với nhau và lưu tiếp kết quả vào [ebp-140]. Và kết quả lại được so sánh qua hàm sub_404000 với [ebp-28]. :arrow_right: input3 =  xor ngược lại [ebp-1F8] và [ebp-28].

Đủ 24 byte của input rồi, nhập input và get flag(hoặc xor input với chuỗi byte tại [ebp-94] để get flag. Sau khi pass qua các bước trên thì chương trình sẽ làm việc này để in flag.) ![level2](https://github.com/hongsonars/mywriteups/blob/master/9str0m2017/level2.py)
