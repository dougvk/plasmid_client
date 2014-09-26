Rails.application.routes.draw do
  get 'home/dashboard', to: 'home#client'

  get 'home/compute'

end
