from django.views.generic import TemplateView, ListView, FormView
from .forms import LogInForm, SIGNUPForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.db.models import Q
from django.views import View
from .forms import ProductForm, ContactForm, ShippingAddressForm, ReviewForm
from .models import Product, ParentCategory, ChildCategory, Cart, Review
from django.http import JsonResponse
import stripe
from django.conf import settings


class HomeView(ListView):
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_featured=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ParentCategory.objects.all()
        context['featuredproducts'] = Product.objects.filter(is_featured=True)
        mobile_category = ParentCategory.objects.get(name='Mobile')
        context['MobileBrands'] = ChildCategory.objects.filter(is_active=True, parent_category=mobile_category, parent_category__is_active=True)
        mobile_category = ParentCategory.objects.get(name='Mobile')
        context['mobileproducts'] = Product.objects.filter(is_active=True, category__parent_category=mobile_category, category__is_active=True)
        tablets_category = ParentCategory.objects.get(name='Tablet')
        context['TabletBrands'] = ChildCategory.objects.filter(is_active=True, parent_category=tablets_category, parent_category__is_active=True)
        tablets_category = ParentCategory.objects.get(name='Tablet')
        context['tabletproducts'] = Product.objects.filter(is_active=True, category__parent_category=tablets_category, category__is_active=True)
        cart_items = Cart.objects.filter(user=self.request.user, is_ordered=False)
        context['cart_items'] = cart_items
        return context


class TabletView(TemplateView):
    template_name = 'tablets.html'
    model = Product
    context_object_name = 'tabletlistings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_category = get_object_or_404(ParentCategory, name='Tablet')
        products = Product.objects.filter(category__parent_category=parent_category)
        tabletcount = Product.objects.filter(category__parent_category=parent_category).count()
        context['tabletcount'] = tabletcount
        context['tabletlistings'] = products
        return context


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class MobilesView(TemplateView):
    template_name = 'mobile_phones.html'
    model = Product
    context_object_name = 'mobilelistings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_category = get_object_or_404(ParentCategory, name='Mobile')
        products = Product.objects.filter(category__parent_category=parent_category)
        mobilecount = Product.objects.filter(category__parent_category=parent_category).count()
        context['mobilecount'] = mobilecount
        context['mobilelistings'] = products
        return context


class AppleAccessoriesView(TemplateView):
    template_name = 'appleaccessories.html'
    context_object_name = 'appleaccessorieslistings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Names of the Apple accessory categories
        apple_accessory_categories = ['Apple TV', 'Apple Phones', 'Apple Tablets', 'Apple Macbook', 'Apple Watches']

        apple_accessories = []
        total_apple_accessories_count = 0

        for category_name in apple_accessory_categories:
            child_category = get_object_or_404(ChildCategory, name=category_name)
            products = Product.objects.filter(category=child_category)
            accessories_count = products.count()
            total_apple_accessories_count += accessories_count
            apple_accessories.append({
                'category_name': category_name,
                'products': products,
                'accessories_count': accessories_count
            })

        context['total_apple_accessories_count'] = total_apple_accessories_count
        context['apple_accessories'] = apple_accessories

        return context


class AppleWatchesView(TemplateView):
    template_name = 'applewatches.html'
    model = Product
    context_object_name = 'applewatchlistings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_category = get_object_or_404(ParentCategory, name='Watches')
        apple_category = get_object_or_404(ChildCategory, name='Apple Watches', parent_category=parent_category)
        products = Product.objects.filter(category=apple_category)
        applewatchcount = Product.objects.filter(category=apple_category).count()
        context['applewatchcount'] = applewatchcount
        context['applewatchlistings'] = products

        return context


class MacbooksView(TemplateView):
    template_name = 'macbooks.html'
    model = Product
    context_object_name = 'macbooklistings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_category = get_object_or_404(ParentCategory, name='Laptop')
        apple_category = get_object_or_404(ChildCategory, name='Apple Macbook', parent_category=parent_category)
        products = Product.objects.filter(category=apple_category)
        applemacbookscount = Product.objects.filter(category=apple_category).count()
        context['applemacbookscount'] = applemacbookscount
        context['macbooklistings'] = products
        return context


class IphonesView(TemplateView):
    template_name = 'Iphones.html'
    model = Product
    context_object_name = 'iphonelistings'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parent_category = get_object_or_404(ParentCategory, name='Mobile')
        apple_category = get_object_or_404(ChildCategory, name='Apple Phones', parent_category=parent_category)
        applephonescount = Product.objects.filter(category=apple_category).count()
        context['applephonescount'] = applephonescount
        products = Product.objects.filter(category=apple_category)
        context['iphonelistings'] = products
        return context


class ContactUsView(FormView):
    template_name = 'contact_us.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CheckOutCartView(ListView):
    template_name = 'checkout_cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user, is_ordered=False)
        else:
            return Cart.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context['cart_items']

        subtotal = 0
        for cart_item in cart_items:
            cart_item.total_price = float(cart_item.product.discounted_price()) * cart_item.quantity
            subtotal += cart_item.total_price

        context['subtotal'] = subtotal
        context['total'] = subtotal
        if 'action' in self.request.POST:
            action = self.request.POST['action']
            cart_item_id = int(self.request.POST['cart_item_id'])
            cart_item = Cart.objects.get(id=cart_item_id)

            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1

            cart_item.total_price = float(cart_item.product.discounted_price()) * cart_item.quantity
            cart_item.save()
            subtotal = 0
            for cart_item in cart_items:
                subtotal += cart_item.total_price

            context['subtotal'] = subtotal
            context['total'] = subtotal

        return context


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'message': 'Product added to cart successfully!'})


class CheckOutCompleteView(TemplateView):
    template_name = 'checkout_complete.html'

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(success=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = kwargs.get('success', False)
        return context


stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckOutPaymentView(TemplateView):
    template_name = 'checkout_payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        cart_items = Cart.objects.filter(user=user, is_ordered=False)
        cart_data = []
        cart_total = 0
        for item in cart_items:
            product = item.product
            cart_data.append({
                'product_name': product.title,
                'quantity': item.quantity,
                'discounted_price': product.discounted_price(),
                'formatted_price': product.formatted_price(),
                # Add more fields as needed
            })
            cart_total += float(product.discounted_price()) * item.quantity
        formatted_cart_total = "{:.2f}".format(cart_total)
        order_total = int(cart_total * 100)
        intent = stripe.PaymentIntent.create(
            amount=order_total,
            currency='usd',
            description="Example charge",
        )
        stripe.Charge.create(
            amount=order_total,
            currency="usd",
            source="tok_amex",
            description="My First Test Charge (created for API docs at https://www.stripe.com/docs/api)",
        )
        context['client_secret'] = intent.client_secret
        context['cart_data'] = cart_data
        context['cart_total'] = formatted_cart_total
        return context


class CheckOutInfoView(FormView):
    template_name = 'checkout_info.html'
    form_class = ShippingAddressForm
    success_url = '/checkoutpayment/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LogInForm
    success_url = '/home/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect("home")
        else:
            messages.error(self.request, "Invalid username or password")
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/login/")


class SignUpView(FormView):
    template_name = 'signup.html'
    form_class = SIGNUPForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class AddProductsView(FormView):
    template_name = 'addproducts.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class FaqView(TemplateView):
    template_name = 'faq.html'


class ProductDetailView(TemplateView):
    template_name = 'product_detail.html'
    form_class = ReviewForm
    success_url = '/'
    model = Review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_name = kwargs['product_name']
        product = get_object_or_404(Product, slug=product_name)
        context['product'] = product
        context['product_description'] = product.product_descriptions.all()
        context['featured_products'] = Product.objects.filter(is_featured=True)
        context['parent_categories'] = ParentCategory.objects.all()
        context['categories'] = ChildCategory.objects.all()
        context['reviews'] = Review.objects.filter(product=product)
        # stars = [{'class': 'fa fa-star', 'value': i} for i in range(1, 6)]
        # context['stars'] = stars
        # for review in context['reviews']:
        #     review.active_stars = range(review.rating)
        #     review.inactive_stars = range(5 - review.rating)
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productdetail', kwargs['product_name'])
        else:
            return redirect('productdetail', kwargs['product_name'])


class ProductListView(ListView):
    template_name = 'product.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products_count'] = Product.objects.count()
        context['categories'] = ParentCategory.objects.all()
        context['products'] = Product.objects.all()[0:9]
        return context


class SearchView(ListView):
    template_name = 'search_results.html'
    model = Product
    context_object_name = 'searched_products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query, 'Search Query!!')
        if query:
            queryset = self.model.objects.filter(
                Q(title__icontains=query))
        else:
            queryset = self.model.objects.all()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = ChildCategory.objects.all()

        return context


# def delete_cart_item(request, product_id):
#     cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user, is_ordered=False)
#     cart_item.delete()
#     return redirect('/')


def delete_cart_item(request, product_id):
    cart_item = get_object_or_404(Cart, product__id=product_id, user=request.user, is_ordered=False)

    if request.method == 'POST':
        product_name = cart_item.product.title
        cart_item.delete()
        return redirect('/')
    else:
        product_name = cart_item.product.title
        context = {
            'product_id': product_id,
            'product_name': product_name,
        }
        return render(request, 'delete_cart_items.html', context)


class MyAccountView(TemplateView):
    template_name = 'my_account.html'


class IndexView(TemplateView):
    template_name = 'index.html'


# class ReviewView(FormView):
#     template_name = 'product_detail.html'
#     form_class = ReviewForm
#     success_url = '/'
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)
