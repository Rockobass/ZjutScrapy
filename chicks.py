# urls = list(map(lambda url: response.urljoin(url), urls))

# os.path.dirname(__file__)  拿到当前目录

# os.path.dirname(os.path.dirname(__file__)) 拿到上级目录

# class BMWImagesPipeline(ImagesPipeline):
#   def get_media_requests(self, item, info):
#     # 这个方法是在发送下载请求之前调用。
#     # 其实这个方法本身就是去发送下载请求的
#     request_objs = super(BMWImagesPipeline, self).get_media_requests(item, info)
#     for request_obj in request_objs:
#       request_obj.item = item
#     return request_objs
#
#   def file_path(self, request, response=None, info=None):
#     # 这个方法是在图片将要被存储的时候调用，来获取这个图片存储的路径
#     path = super(BMWImagesPipeline, self).file_path(request, response, info)
#     category = request.item.get('category')
#     images_store = settings.IMAGES_STORE
#     category_path = os.path.join(images_store, category)
#     if not os.path.exists(category_path):
#       os.mkdir(category_path)
#     image_name = path.replace("full/", "")
#     image_path = os.path.join(category_path, image_name)
#     return image_path