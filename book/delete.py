import book
from book.models import WishBookList

instance = WishBookList.objects.get(id=1)
instance.delete()
