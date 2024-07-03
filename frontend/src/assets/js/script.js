$(document).ready(function() {
    $('#mobile_btn').on('click', function () {
        $('#mobile_menu').toggleClass('active');
        $('#mobile_btn').find('i').toggleClass('fa-x');
    });

    const sections = $('section');
    const navItems = $('.link');

    $(window).on('scroll', function () {
        const nav = $('nav');
        const scrollPosition = $(window).scrollTop() - nav.outerHeight();

        let activeSectionIndex = 0;

        if (scrollPosition <= 0) {
            nav.css('box-shadow', 'none');
        } else {
            nav.css('box-shadow', '5px 1px 5px rgba(0, 0, 0, 0.1');
        }

        sections.each(function(i) {
            const section = $(this);
            const sectionTop = section.offset().top - 56;
            const sectionBottom = sectionTop+ section.outerHeight();

            if (scrollPosition >= sectionTop && scrollPosition < sectionBottom) {
                activeSectionIndex = i;
                return false;
            }
        })

        navItems.removeClass('active');
        $(navItems[activeSectionIndex]).addClass('active');
    });

       
      ScrollReveal().reveal('.headline', {
        origin: 'left',
        duration: 2000,
        distance: '20%'
    });
    ScrollReveal().reveal('.ds', {
        origin: 'left',
        duration: 3000,
        distance: '20%'
    });
    ScrollReveal().reveal('.imagem1', {
        origin: 'botton',
        duration: 2000,
        distance: '20%'
    });
    ScrollReveal().reveal('.imagem2', {
        origin: 'top',
        duration: 2000,
        distance: '40%'
    });

    ScrollReveal().reveal('#inteligencia_integro', {
        origin: 'right',
        duration: 2000,
        distance: '20%'
    });
    ScrollReveal().reveal('#titulo_integro', {
        origin: 'top',
        duration: 2000,
        distance: '20%'
    });
    ScrollReveal().reveal('#descrito_integro', {
        origin: 'left',
        duration: 2000,
        distance: '20%'
    });
    ScrollReveal().reveal('#banner1', {
        origin: 'right',
        duration: 2000,
        distance: '20%'
    });
    ScrollReveal().reveal('#descrition', {
        origin: 'bottom',
        duration: 2000,
        distance: '20%'
    });

    
    ScrollReveal().reveal('#banner2', {
        origin: 'top',
        duration: 2000,
        distance: '20%'
    });

    ScrollReveal().reveal('#testimonial_chef', {
        origin: 'left',
        duration: 1000,
        distance: '20%'
    })

    ScrollReveal().reveal('.feedback', {
        origin: 'right',
        duration: 1000,
        distance: '20%'
    })
});