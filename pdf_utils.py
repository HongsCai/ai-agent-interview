import pdfplumber
import io


def extract_text_from_pdf(file_source):
    """
    解析PDF文件并提取文本
    :param file_source: 文件路径(str) 或 文件对象(FileStorage/BytesIO)
    :return: 提取出的字符串文本
    """
    text_content = []

    try:
        # pdfplumber.open 支持文件路径或文件流
        with pdfplumber.open(file_source) as pdf:
            # 遍历每一页
            for i, page in enumerate(pdf.pages):
                # 提取文本
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                else:
                    print(f"第 {i + 1} 页没有提取到文本 (可能是图片扫描件)")

        # 将所有页面的文本用换行符拼接
        return "\n".join(text_content)

    except Exception as e:
        print(f"PDF解析发生错误: {e}")
        return None


# 测试代码（如果你想单独运行这个文件测试的话）
if __name__ == '__main__':
    # 假设你有一个本地文件 test.pdf
    # print(PdfUtils.extract_text_from_pdf("test.pdf"))
    pass