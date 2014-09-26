class HomeController < ApplicationController
  require 'httparty'
  #skip_before_action :verify_authenticity_token
  #before_filter :authenticate, only: [:client]

  def client
  end

  def compute
    response = HTTParty.post('http://162.243.29.17/%s/service' % params['client'],
                            body: {categories: params['categories'],
                                   basket_size: params['basket_size'],
                                   demographics: params['demographics']})
    @result = JSON.parse(response.body)
    render json: @result
  end

  protected

  def authenticate
      authenticate_or_request_with_http_basic do |username, password|
            username == ENV['HTACCESS_USERNAME'] && password == ENV['HTACCESS_PASSWORD']
      end
  end
end
