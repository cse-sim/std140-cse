# OpenStudio
# Copyright (c) 2008-2010, Alliance for Sustainable Energy.  All rights reserved.
# See the file "License.txt" for additional terms and conditions.


module OpenStudio

  class FieldDefinition

    attr_accessor :name, :type, :default_value, :required, :units_si, :units_ip, :object_list, :object_list_keys, :choice_keys, :autosizable

    def initialize
      @name = ""      # \field
      @type = ""      # A or N
      @default_value = nil  # \default, nil indicates no default
      @required = false
      @units_si = ""  # \units
      @units_ip = ""  # \ip-units
      @object_list = ""  # \object-list, reference to another object
      @object_list_keys = []  # \reference, array of keys that can be referenced by \object-list
      @choice_keys = []  # \choice, array of fixed choice keys
      @autosizable = false # \autosizable
    end
    
    
    def get_choice_key(key_name)
      actual_key = nil
      for key in @choice_keys
        if (key.upcase == key_name.upcase)
          actual_key = key
          break
        end
      end
      return(actual_key)
    end


    def inspect
      return(to_s)
    end


    def autosizable?
      @autosizable
    end

  end
  
end