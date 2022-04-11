from django.test import TestCase
from lists.models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")


class NewListTest(TestCase):
    def test_redirects_after_post(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        new_list = List.objects.first()
        self.assertRedirects(response, f"/lists/{new_list.id}/")

    def test_can_save_a_post_request(self):
        self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")


class ListAndItemModelsTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()
        first_item = Item()
        first_item.text = "The first item"
        first_item.list = list_
        first_item.save()
        second_item = Item()
        second_item.text = "item 2"
        second_item.list = list_
        second_item.save()
        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, "The first item")
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, "item 2")
        self.assertEqual(second_saved_item.list, list_)


class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_display_only_items_for_that_list(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1", list=list_)
        Item.objects.create(text="itemey 2", list=list_)
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        other = List.objects.create()
        Item.objects.create(text="other item 1", list=other)
        Item.objects.create(text="other item 2", list=other)
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertContains(response, "itemey 1")
        self.assertContains(response, "itemey 2")
        self.assertNotContains(response, "other item 1")
        self.assertNotContains(response, "other item 2")

    def test_passes_correct_list_to_template(self):
        other = List.objects.create()
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertEqual(response.context["list"], list_)


class NewItemTest(TestCase):
    def test_can_save_a_post_request_to_an_existing_list(self):
        other = List.objects.create()
        list_ = List.objects.create()
        item_text = "A new item for an existing list"
        self.client.post(f"/lists/{list_.id}/add_item", data={"item_text": item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, item_text)
        self.assertEqual(new_item.list, list_)

    def test_redirects_to_list_view(self):
        other = List.objects.create()
        list_ = List.objects.create()
        item_text = "A new item for an existing list"
        response = self.client.post(
            f"/lists/{list_.id}/add_item", data={"item_text": item_text}
        )
        self.assertRedirects(response, f"/lists/{list_.id}/")
