# Lab 7 - YummyApp CI/CD

## Chay cuc bo

```powershell
python -m pip install -r requirements.txt
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
python -m coverage run --source=yummy_app,gps_service -m unittest discover -s . -p "test_*.py"
python -m coverage report -m
python -m coverage html -d coverage_html
python -m coverage report --fail-under=80
```

Workflow GitHub Actions trong `.github/workflows/yummyapp-ci.yml` chay cung linter,
bo test, quality gate 80% va upload HTML coverage report.

## Minh chung can bo sung truoc khi nop

Thu muc nay chua the xem la goi nop bai cuoi cung. Cac minh chung sau phai duoc tao
tu thao tac that cua sinh vien, khong duoc thay bang file gia lap:

- `logs/git_history.log`: tao sau khi commit bang tai khoan/thong tin tac gia cua ban.
- `logs/github_actions_run.log`: tai raw log cua mot workflow run thanh cong tren GitHub.
- `MinhChung_VietTay_2312634.pdf`: scan/chup bon trang viet tay co ho ten, MSSV,
  ngay lam bai va chu ky tuoi.
- `BaoCao_KetQua_Lab7.pdf`: bao cao co link repository GitHub that va anh chup minh chung.

Truoc khi nop, dat hai file PDF tren vao thu muc nay. Sau khi co cac minh chung that,
nen zip toan bo thu muc `2312634_PhanThanhHuy_Lab7` thanh
`2312634_PhanThanhHuy_Lab7.zip`. Khong dua `.coverage`, `__pycache__` hoac
`coverage_html/` vao file nop; coverage HTML duoc GitHub Actions luu thanh artifact.
