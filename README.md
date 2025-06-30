노션 가이드를 따라하시면 됩니다.<br />
https://www.notion.so/wakeup-vosk-21f459e1ac2b80fcb491da2442ed2ae5?source=copy_link<br /><br />

**Hi-Telly_en_raspberry-pi_v3_0_0.zip**<br />
.zip파일은 "Hi Telly"를 wake up word로 만들어 주기 위한 엔진 파일들입니다. 압축 해제시켜 주시면 됩니다.

**realtime_test.py**<br />
vosk를 통해 실시간 음성 인식이 되는지 확인할 수 있는 코드입니다. 
여기에는 포쿠파인을 통한 wake up 기능은 없습니다. (단순 STT 테스트)

**wake_and_listen_repeat.py**<br />
Hi Telly 를 인식하면, 뒤에 말하는 한 문장을 텍스트로 바꿔주는 프로그램입니다.
